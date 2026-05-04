#!/usr/bin/env python3
"""
Compare base model vs SFT LoRA model on the validation set.

Metrics:
  1. json_valid_rate     - % of outputs that are valid JSON
  2. field_hit_rate      - % of required JSON fields present (per task type)
  3. rouge_l             - ROUGE-L F1 vs reference output
  4. tool_accuracy       - for tool-call tasks: correct tool name selected
  5. file_mention_rate   - for swebench_plan tasks: expected file mentioned
  6. patch_format_rate   - for patch tasks: output contains unified diff marker
  7. avg_tokens_per_sec  - inference speed

Usage:
    conda run -n liuyang_aihigh python scripts/eval_before_after_sft.py \\
        --base-model models/Qwen3-8B \\
        --adapter-dir outputs/qwen_supported_coding_agent_lora_llamafactory \\
        --val-data data/llamafactory/val_alpaca.json \\
        --max-new-tokens 512 \\
        --output-dir outputs/eval_results
"""

import argparse
import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _device_map_arg(device: str):
    """Return device_map for from_pretrained. Use 'auto' for multi-GPU."""
    if device == "auto" or "," in device:
        return "auto"
    return device


def _input_device(model):
    """Return the device of the first model parameter (for input placement)."""
    return next(model.parameters()).device


def load_adapter_model(base_model_path: str, adapter_dir: str, device: str):
    """Load base model with LoRA adapter via PEFT."""
    from peft import PeftModel
    logger.info(f"Loading base model from {base_model_path} ...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        dtype=torch.bfloat16,
        device_map=_device_map_arg(device),
        trust_remote_code=True,
    )
    # Find latest checkpoint if adapter_dir is the output root
    adapter_path = Path(adapter_dir)
    checkpoints = sorted(adapter_path.glob("checkpoint-*"), key=lambda p: int(p.name.split("-")[1]))
    if checkpoints:
        final_ckpt = checkpoints[-1]
        logger.info(f"Using adapter checkpoint: {final_ckpt}")
        adapter_path = final_ckpt

    logger.info(f"Loading LoRA adapter from {adapter_path} ...")
    model = PeftModel.from_pretrained(model, str(adapter_path))
    model.eval()
    return tokenizer, model


def load_base_model(base_model_path: str, device: str):
    logger.info(f"Loading base model from {base_model_path} ...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        dtype=torch.bfloat16,
        device_map=_device_map_arg(device),
        trust_remote_code=True,
    )
    model.eval()
    return tokenizer, model


def build_prompt(tokenizer, system: str, instruction: str, input_text: str) -> str:
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"{instruction}\n\n{input_text}" if input_text else instruction},
    ]
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


@torch.inference_mode()
def generate_responses(
    tokenizer,
    model,
    samples: list[dict],
    max_new_tokens: int,
    device: str,
) -> tuple[list[str], float]:
    """Return (responses, avg_tokens_per_sec)."""
    responses = []
    total_tokens = 0
    total_time = 0.0
    input_dev = _input_device(model)  # works for both single-GPU and device_map="auto"

    for i, sample in enumerate(samples):
        prompt = build_prompt(
            tokenizer,
            sample.get("system", ""),
            sample["instruction"],
            sample.get("input", ""),
        )
        inputs = tokenizer(prompt, return_tensors="pt").to(input_dev)
        input_len = inputs["input_ids"].shape[1]

        t0 = time.perf_counter()
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            top_p=None,
            pad_token_id=tokenizer.eos_token_id,
        )
        elapsed = time.perf_counter() - t0

        new_tokens = output_ids[0][input_len:]
        response = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        responses.append(response)

        n_new = len(new_tokens)
        total_tokens += n_new
        total_time += elapsed

        if (i + 1) % 5 == 0 or i == len(samples) - 1:
            logger.info(f"  [{i+1}/{len(samples)}] generated {n_new} tokens in {elapsed:.2f}s")

    avg_tps = total_tokens / total_time if total_time > 0 else 0.0
    return responses, avg_tps


# ---------------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------------

def is_valid_json(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except Exception:
        return False


def parse_json_safe(text: str) -> dict | None:
    try:
        return json.loads(text)
    except Exception:
        # Try to extract JSON from text
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except Exception:
                pass
    return None


def rouge_l_f1(prediction: str, reference: str) -> float:
    """Compute ROUGE-L F1 using LCS."""
    pred_tokens = prediction.lower().split()
    ref_tokens = reference.lower().split()
    if not pred_tokens or not ref_tokens:
        return 0.0
    # LCS length via DP
    m, n = len(ref_tokens), len(pred_tokens)
    # Use O(n) space
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if ref_tokens[i - 1] == pred_tokens[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    lcs = prev[n]
    precision = lcs / n if n > 0 else 0.0
    recall = lcs / m if m > 0 else 0.0
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def detect_task_type(instruction: str) -> str:
    if "修复计划" in instruction or "制定" in instruction and "计划" in instruction:
        return "swebench_plan"
    if "unified diff" in instruction or "修复补丁" in instruction or "patch" in instruction.lower():
        return "swebench_patch"
    if "工具轨迹" in instruction or "下一步工具调用" in instruction:
        return "tool_call"
    if "执行最小工具调用策略" in instruction or "strategy" in instruction.lower():
        return "strategy"
    return "other"


TASK_REQUIRED_FIELDS = {
    "swebench_plan": ["plan", "validation"],
    "swebench_patch": ["patch"],
    "tool_call": ["tool", "arguments"],
    "strategy": ["strategy"],
    "other": [],
}


def compute_field_hit_rate(pred_json: dict | None, task_type: str) -> float:
    required = TASK_REQUIRED_FIELDS.get(task_type, [])
    if not required:
        return 1.0
    if pred_json is None:
        return 0.0
    hits = sum(1 for f in required if f in pred_json)
    return hits / len(required)


def compute_tool_accuracy(pred_json: dict | None, ref_json: dict | None) -> float | None:
    if pred_json is None or ref_json is None:
        return None
    pred_tool = pred_json.get("tool", "").strip().lower()
    ref_tool = ref_json.get("tool", "").strip().lower()
    if not ref_tool:
        return None
    return 1.0 if pred_tool == ref_tool else 0.0


def compute_file_mention_rate(pred_text: str, ref_json: dict | None) -> float | None:
    """Check if the expected file(s) from the reference plan appear in the prediction."""
    if ref_json is None:
        return None
    ref_plan = ref_json.get("plan", "")
    # Extract file paths from reference plan (e.g. "django/forms/boundfield.py")
    files = re.findall(r'[\w/]+\.py', ref_plan)
    if not files:
        return None
    hits = sum(1 for f in files if f in pred_text)
    return hits / len(files)


# ---------------------------------------------------------------------------
# Main evaluation
# ---------------------------------------------------------------------------

def evaluate(responses: list[str], samples: list[dict]) -> dict[str, Any]:
    json_valid = []
    rouge_scores = []
    field_hits = []
    tool_accs = []
    file_mentions = []
    patch_format = []

    for resp, sample in zip(responses, samples):
        ref_text = sample["output"]
        task_type = detect_task_type(sample["instruction"])

        # 1. JSON validity
        json_valid.append(1 if is_valid_json(resp) else 0)

        # 2. ROUGE-L vs reference
        rouge_scores.append(rouge_l_f1(resp, ref_text))

        # 3. Field hit rate
        pred_json = parse_json_safe(resp)
        ref_json = parse_json_safe(ref_text)
        field_hits.append(compute_field_hit_rate(pred_json, task_type))

        # 4. Tool accuracy (tool_call tasks)
        if task_type == "tool_call":
            acc = compute_tool_accuracy(pred_json, ref_json)
            if acc is not None:
                tool_accs.append(acc)

        # 5. File mention rate (swebench_plan tasks)
        if task_type == "swebench_plan":
            rate = compute_file_mention_rate(resp, ref_json)
            if rate is not None:
                file_mentions.append(rate)

        # 6. Patch format (swebench_patch tasks)
        if task_type == "swebench_patch":
            patch_format.append(1 if "diff --git" in resp else 0)

    def safe_mean(lst):
        return sum(lst) / len(lst) if lst else None

    return {
        "n_samples": len(samples),
        "json_valid_rate": safe_mean(json_valid),
        "rouge_l": safe_mean(rouge_scores),
        "field_hit_rate": safe_mean(field_hits),
        "tool_accuracy": safe_mean(tool_accs),
        "file_mention_rate": safe_mean(file_mentions),
        "patch_format_rate": safe_mean(patch_format),
        # counts for context
        "_n_tool_call": len(tool_accs),
        "_n_swebench_plan": len(file_mentions),
        "_n_patch": len(patch_format),
    }


def print_comparison(base_metrics: dict, sft_metrics: dict):
    metric_labels = {
        "json_valid_rate":    "JSON 格式正确率    ",
        "field_hit_rate":     "必填字段命中率      ",
        "rouge_l":            "ROUGE-L (vs ref)    ",
        "tool_accuracy":      "Tool 选择准确率     ",
        "file_mention_rate":  "文件命中率(swebench)",
        "patch_format_rate":  "Patch 格式正确率    ",
    }

    print("\n" + "=" * 64)
    print(f"{'指标':<26} {'Base':>10} {'SFT':>10} {'Delta':>10}")
    print("-" * 64)
    for key, label in metric_labels.items():
        bv = base_metrics.get(key)
        sv = sft_metrics.get(key)
        if bv is None and sv is None:
            continue
        bv_str = f"{bv*100:.1f}%" if bv is not None else "  N/A"
        sv_str = f"{sv*100:.1f}%" if sv is not None else "  N/A"
        if bv is not None and sv is not None:
            delta = sv - bv
            delta_str = f"{delta*100:+.1f}%"
        else:
            delta_str = "  N/A"
        print(f"{label:<26} {bv_str:>10} {sv_str:>10} {delta_str:>10}")
    print("=" * 64)
    print(f"  样本数: {base_metrics['n_samples']}  "
          f"(tool_call={base_metrics['_n_tool_call']}, "
          f"swebench_plan={base_metrics['_n_swebench_plan']}, "
          f"patch={base_metrics['_n_patch']})")
    print("=" * 64 + "\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="Evaluate base vs SFT model on validation set.")
    p.add_argument("--base-model", default="models/Qwen3-8B",
                   help="Path to base model")
    p.add_argument("--adapter-dir",
                   default="outputs/qwen_supported_coding_agent_lora_llamafactory",
                   help="Path to LLaMA-Factory output dir (will pick latest checkpoint)")
    p.add_argument("--val-data", default="data/llamafactory/val_alpaca.json",
                   help="Validation data in alpaca format")
    p.add_argument("--max-new-tokens", type=int, default=512)
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--output-dir", default="outputs/eval_results",
                   help="Directory to save detailed results JSON")
    p.add_argument("--skip-base", action="store_true",
                   help="Skip base model evaluation (load saved base results)")
    return p.parse_args()


def main():
    args = parse_args()

    # Resolve relative paths from the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    val_data_path = project_root / args.val_data
    adapter_dir = project_root / args.adapter_dir
    output_dir = project_root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load validation data
    logger.info(f"Loading validation data from {val_data_path}")
    with open(val_data_path) as f:
        samples = json.load(f)
    logger.info(f"Loaded {len(samples)} validation samples")

    # ---- Base model ----
    base_results_path = output_dir / "base_responses.json"
    if args.skip_base and base_results_path.exists():
        logger.info("Skipping base model, loading saved results ...")
        with open(base_results_path) as f:
            saved = json.load(f)
        base_responses = saved["responses"]
        base_tps = saved["avg_tokens_per_sec"]
    else:
        tokenizer_base, model_base = load_base_model(args.base_model, args.device)
        logger.info("Running inference with BASE model ...")
        base_responses, base_tps = generate_responses(
            tokenizer_base, model_base, samples, args.max_new_tokens, args.device
        )
        with open(base_results_path, "w") as f:
            json.dump({"responses": base_responses, "avg_tokens_per_sec": base_tps}, f, ensure_ascii=False, indent=2)
        del model_base
        torch.cuda.empty_cache()

    # ---- SFT model ----
    tokenizer_sft, model_sft = load_adapter_model(args.base_model, str(adapter_dir), args.device)
    logger.info("Running inference with SFT model ...")
    sft_responses, sft_tps = generate_responses(
        tokenizer_sft, model_sft, samples, args.max_new_tokens, args.device
    )
    sft_results_path = output_dir / "sft_responses.json"
    with open(sft_results_path, "w") as f:
        json.dump({"responses": sft_responses, "avg_tokens_per_sec": sft_tps}, f, ensure_ascii=False, indent=2)

    # ---- Metrics ----
    logger.info("Computing metrics ...")
    base_metrics = evaluate(base_responses, samples)
    sft_metrics = evaluate(sft_responses, samples)
    base_metrics["avg_tokens_per_sec"] = base_tps
    sft_metrics["avg_tokens_per_sec"] = sft_tps

    # Save detailed results
    detailed = []
    for i, (sample, br, sr) in enumerate(zip(samples, base_responses, sft_responses)):
        detailed.append({
            "idx": i,
            "task_type": detect_task_type(sample["instruction"]),
            "instruction": sample["instruction"][:100],
            "reference": sample["output"],
            "base_response": br,
            "sft_response": sr,
            "base_rouge_l": rouge_l_f1(br, sample["output"]),
            "sft_rouge_l": rouge_l_f1(sr, sample["output"]),
            "base_json_valid": is_valid_json(br),
            "sft_json_valid": is_valid_json(sr),
        })
    with open(output_dir / "detailed_results.json", "w") as f:
        json.dump(detailed, f, ensure_ascii=False, indent=2)

    # ---- Print comparison table ----
    print("\n>>> BASE MODEL:")
    print(f"    Avg tokens/sec: {base_tps:.1f}")
    print("\n>>> SFT MODEL:")
    print(f"    Avg tokens/sec: {sft_tps:.1f}")
    print_comparison(base_metrics, sft_metrics)

    # Save metrics summary
    with open(output_dir / "metrics_summary.json", "w") as f:
        json.dump({"base": base_metrics, "sft": sft_metrics}, f, ensure_ascii=False, indent=2)
    logger.info(f"Results saved to {output_dir}")


if __name__ == "__main__":
    main()
