from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

SYSTEM_PROMPT = """你是一个 Claude Code 风格的代码仓库 Agent。
你需要根据用户任务、仓库上下文和历史工具轨迹，输出严格可解析的 JSON。
优先选择最小、安全、可测试的修改方案。"""

DEFAULT_INPUTS = [
    "data/sft/agent_traces_sft.jsonl",
    "data/sft/swebench_lite_plan_sft.jsonl",
    "data/sft/mbpp_strategy_sft.jsonl",
    "data/sft/mbpp_sft.jsonl",
    "data/sft/humaneval_sft.jsonl",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert project SFT data into LLaMA-Factory alpaca format.")
    parser.add_argument("--inputs", nargs="*", default=DEFAULT_INPUTS)
    parser.add_argument("--output-dir", default="data/llamafactory")
    parser.add_argument("--train-ratio", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rows: list[dict[str, Any]] = []
    stats: dict[str, int] = {}
    for input_file in args.inputs:
        path = Path(input_file)
        if not path.exists():
            continue
        count = 0
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows.append(convert_record(item, path.name))
            count += 1
        stats[path.name] = count

    random.Random(args.seed).shuffle(rows)
    split = int(len(rows) * args.train_ratio)
    train = rows[:split]
    val = rows[split:]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    train_path = output_dir / "train_alpaca.json"
    val_path = output_dir / "val_alpaca.json"
    dataset_info_path = output_dir / "dataset_info.json"
    stats_path = output_dir / "dataset_stats.json"

    train_path.write_text(json.dumps(train, ensure_ascii=False, indent=2), encoding="utf-8")
    val_path.write_text(json.dumps(val, ensure_ascii=False, indent=2), encoding="utf-8")
    dataset_info = {
        "coding_agent_train": {
            "file_name": train_path.name,
            "formatting": "alpaca",
            "columns": {
                "prompt": "instruction",
                "query": "input",
                "response": "output",
                "system": "system",
            },
        },
        "coding_agent_val": {
            "file_name": val_path.name,
            "formatting": "alpaca",
            "columns": {
                "prompt": "instruction",
                "query": "input",
                "response": "output",
                "system": "system",
            },
        },
    }
    dataset_info_path.write_text(json.dumps(dataset_info, ensure_ascii=False, indent=2), encoding="utf-8")
    stats_payload = {"total": len(rows), "train": len(train), "val": len(val), "inputs": stats}
    stats_path.write_text(json.dumps(stats_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(stats_payload, ensure_ascii=False, indent=2))
    print(f"train={train_path}")
    print(f"val={val_path}")
    print(f"dataset_info={dataset_info_path}")


def convert_record(record: dict[str, Any], source: str) -> dict[str, str]:
    instruction = str(record.get("instruction", "根据输入完成任务。"))
    user_input = record.get("input", {})
    output = record.get("output", {})
    return {
        "system": SYSTEM_PROMPT,
        "instruction": f"{instruction}\n\n来源文件: {source}",
        "input": json.dumps(user_input, ensure_ascii=False, indent=2),
        "output": json.dumps(output, ensure_ascii=False, indent=2),
    }


if __name__ == "__main__":
    main()
