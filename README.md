# Coding Agent SFT Lab

A lightweight repository coding agent with an integrated SFT data pipeline — run, trace, and train.

Built with [LangGraph](https://github.com/langchain-ai/langgraph), this project gives you a Claude Code-style agent that inspects files, makes safe edits, runs tests, and logs every decision. Its companion pipeline converts benchmark datasets and agent traces into supervised fine-tuning data, ready for LLaMA-Factory training.

## Quick Start

```bash
# Install runtime dependencies
pip install -r requirements.txt

# Configure your LLM (OpenAI-compatible API)
cp .env.example .env
# Edit .env: set OPENAI_API_KEY, OPENAI_BASE_URL (optional), OPENAI_MODEL
```

### Run the Agent

```bash
python run_agent.py run --repo ./examples/sample_repo --task "修复 subtract 函数" --test-command "pytest -q"
```

The agent follows a **Plan -> Act -> Verify -> Review -> Summarize** loop, writing a JSONL trace of every step.

### Index a Repository

```bash
python run_agent.py index --repo ./examples/sample_repo --query "subtract bug"
python run_agent.py retrieve --repo ./examples/sample_repo --query "calculator functions"
```

### Summarize Traces

```bash
python run_agent.py stats --path traces/
```

## Agent Tools

| Tool             | Description                                      |
| ---------------- | ------------------------------------------------ |
| `list_files`     | List files under a path                          |
| `read_file`      | Read a text file                                 |
| `grep`           | Search with regex                                |
| `retrieve_context` | Lexical retrieval over the repository          |
| `replace_in_file` | Focused exact-string replacement               |
| `write_file`     | Full-file overwrite                              |
| `run_tests`      | Execute allowlisted test commands                |
| `git_diff`       | Show working-tree diff                           |
| `finish`         | Signal task completion                           |

All tools are confined to the target repository. Destructive commands and protected files (`.env`, keys, generated directories) are automatically blocked.

## SFT Data Pipeline

Build training data from benchmarks and agent trajectories:

```bash
# Download and build mini-repos + SFT samples from public benchmarks
python run_agent.py build-humaneval --limit 50
python run_agent.py build-mbpp --limit 50

# Build task manifest from SWE-bench Lite metadata
python run_agent.py build-swebench-lite --limit 50

# Convert agent traces to tool-call SFT samples
python run_agent.py traces-to-sft --trace-path traces/

# Convert local task manifests to strategy SFT samples
python run_agent.py local-tasks-to-sft --input data/tasks/mbpp_tasks.jsonl

# Convert SWE-bench manifests to patch/plan SFT samples
python run_agent.py swebench-to-sft --mode patch
```

### Run Batch Tasks

```bash
# Dry-run: validate which tasks are runnable
python run_agent.py run-tasks --manifest data/tasks/mbpp_tasks.jsonl --limit 5 --dry-run

# Full run: execute each task through the agent and produce traces
python run_agent.py run-tasks --manifest data/tasks/mbpp_tasks.jsonl --limit 5
```

## SFT Training

Scripts in [`scripts/`](scripts/) prepare and launch fine-tuning with LLaMA-Factory:

| Script                                      | Purpose                                     |
| ------------------------------------------- | ------------------------------------------- |
| `install_llamafactory.sh`                   | Install LLaMA-Factory and dependencies       |
| `prepare_llamafactory_sft.py`               | Convert SFT JSONL into LLaMA-Factory format  |
| `download_qwen_model.sh` / `download_hf_model.py` | Download base models                    |
| `train_qwen_supported_llamafactory_lora.sh`   | Launch LoRA fine-tuning on Qwen            |
| `eval_before_after_sft.py`                  | Compare model performance before/after SFT   |

Typical workflow:

```bash
# 1. Prepare training data
bash scripts/install_llamafactory.sh
python scripts/prepare_llamafactory_sft.py --input data/sft/agent_traces_sft.jsonl

# 2. Train
bash scripts/train_qwen_supported_llamafactory_lora.sh

# 3. Evaluate
python scripts/eval_before_after_sft.py
```

## Configuration

Set via environment variables or `.env`:

| Variable                 | Default        | Description                     |
| ------------------------ | -------------- | ------------------------------- |
| `OPENAI_API_KEY`         | —              | API key (required)              |
| `OPENAI_BASE_URL`        | OpenAI default | Custom endpoint                 |
| `OPENAI_MODEL`           | `gpt-4o-mini`  | Model name                      |
| `OPENAI_TEMPERATURE`     | `0.1`          | Sampling temperature            |
| `CC_AGENT_MAX_STEPS`     | `8`            | Max agent loop iterations       |
| `CC_AGENT_COMMAND_TIMEOUT` | `60`         | Shell command timeout (seconds) |
| `CC_AGENT_TRACE_DIR`     | `traces`       | Trace output directory          |

## Project Structure

```
.
├── run_agent.py                # CLI entry point
├── src/cc_agent/               # Agent package
│   ├── cli.py                  # Typer CLI commands
│   ├── graph.py                # LangGraph agent graph
│   ├── tools.py                # Safe tool implementations
│   ├── hooks.py                # Safety validators
│   ├── repo_indexer.py         # Lexical repo indexing & retrieval
│   ├── data_builder.py         # SFT data construction pipeline
│   ├── task_runner.py          # Batch task execution
│   ├── tracing.py / trace_stats.py  # JSONL tracing & metrics
│   ├── config.py / llm.py      # Configuration & LLM client
│   └── state.py / json_utils.py    # Agent state & JSON helpers
├── scripts/                    # SFT training & eval scripts
├── examples/
│   ├── benchmark_tasks.json    # Sample task manifest
│   └── sample_repo/            # Sample repo with buggy calculator
└── data/                       # Generated datasets, tasks, SFT files
```

## Example Task Manifest

```json
[
  {
    "id": "sample_subtract_fix",
    "repo": "examples/sample_repo",
    "task": "修复 subtract 函数的错误实现，并运行测试",
    "test_command": "pytest -q"
  }
]
```

Run it with `python run_agent.py run-tasks --manifest examples/benchmark_tasks.json --limit 1`.

## Requirements

- Python 3.10+
- OpenAI-compatible API endpoint
- Optional: `datasets` for benchmark downloads, `torch` + `transformers` + `peft` for SFT training
