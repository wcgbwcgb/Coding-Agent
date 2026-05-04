# Qwen3-8B Agent SFT 实验报告

本报告总结 Code Agent 项目的 SFT 小实验闭环：数据构建 → LLaMA-Factory 格式转换 → Qwen3-8B LoRA SFT → 微调前后评估。

## 1. 实验目标

目标不是训练生产级 Coding Agent，而是验证小规模 Agent 数据能否显著提升模型对结构化输出协议的遵循能力。

实验链路：

```text
Agent traces / code benchmark data
  → data/sft/*.jsonl
  → data/llamafactory/*.json
  → Qwen3-8B LoRA SFT
  → base vs SFT evaluation
```

## 2. 数据

本次转换使用 724 条样本：

| 数据源 | 数量 | 作用 |
| --- | ---: | --- |
| `agent_traces_sft.jsonl` | 124 | 学习工具调用 JSON 格式 |
| `swebench_lite_plan_sft.jsonl` | 300 | 学习 issue → 修复计划 |
| `mbpp_strategy_sft.jsonl` | 100 | 学习本地任务策略 |
| `mbpp_sft.jsonl` | 100 | 学习基础代码生成 |
| `humaneval_sft.jsonl` | 100 | 学习函数级代码生成 |

转换后：

| Split | 数量 |
| --- | ---: |
| train | 687 |
| val | 37 |

## 3. 训练配置

| 项目 | 配置 |
| --- | --- |
| Base model | `Qwen/Qwen3-8B` |
| Framework | LLaMA-Factory |
| Fine-tuning | LoRA SFT |
| LoRA rank / alpha | 8 / 32 |
| Effective batch size | 16 |
| cutoff_len | 4096 |
| learning rate | `1e-4` |
| epoch | 1 |
| dtype | bf16 |

参数规模：

| 项目 | 数值 |
| --- | ---: |
| 总参数量 | 8,212,558,848 |
| 可训练参数量 | 21,823,488 |
| 可训练比例 | 0.2657% |

训练结果：

| 指标 | 数值 |
| --- | ---: |
| global step | 43 |
| train runtime | 327.33 秒 |
| final train loss | 0.7430 |

## 4. Loss 变化

| step | loss |
| ---: | ---: |
| 5 | 2.2388 |
| 10 | 1.2197 |
| 15 | 0.8163 |
| 20 | 0.5711 |
| 25 | 0.3934 |
| 30 | 0.2718 |
| 35 | 0.3352 |
| 40 | 0.3495 |

loss 在前 30 step 下降明显，说明模型很快学会了当前数据集的输出模板；后半段略有波动，提示小数据集存在过拟合风险。

## 5. 评估指标

评估脚本：`scripts/eval_before_after_sft.py`

| 指标 | 含义 |
| --- | --- |
| `json_valid_rate` | 输出是否为合法 JSON |
| `field_hit_rate` | 必填字段是否存在 |
| `rouge_l` | 与参考答案的 ROUGE-L F1 |
| `tool_accuracy` | 工具调用任务中 tool 名称是否正确 |
| `file_mention_rate` | SWE-bench plan 中是否命中关键文件 |

验证集任务分布：

| 类型 | 数量 |
| --- | ---: |
| `swebench_plan` | 13 |
| `tool_call` | 20 |
| `strategy` | 4 |

## 6. 微调前后结果

| 指标 | Base | SFT | 提升 |
| --- | ---: | ---: | ---: |
| JSON 格式正确率 | 0.0% | 94.6% | +94.6% |
| 必填字段命中率 | 1.4% | 94.6% | +93.2% |
| ROUGE-L | 10.1% | 73.1% | +63.0% |
| Tool 选择准确率 | 0.0% | 83.3% | +83.3% |
| 文件命中率 | 7.7% | 38.5% | +30.8% |

代表性现象：base model 倾向输出自然语言解释或推理过程；SFT model 更倾向直接输出目标 JSON，例如：

```json
{
  "plan": "Inspect and modify these likely relevant files: django/core/management/base.py...",
  "validation": "Use SWE-bench harness and the provided test_patch to validate the fix."
}
```

## 7. 结论

本次实验证明：小规模、高一致性的 Agent SFT 数据能显著提升 Qwen3-8B 对结构化 JSON 输出协议和工具调用格式的遵循能力。

需要谨慎解读的是：该实验主要验证“输出协议对齐”，不能直接说明模型真实修复复杂代码的能力同幅度提升。后续需要扩大 held-out 测试集、加入 patch 执行评估，并做端到端 Agent loop 验证。

## 8. 下一步

- 扩充高质量 Agent traces 到 500-1000 条以上。
- 增加真实 patch 样本和测试执行指标。
- 构造独立 held-out 测试集，避免同分布评估偏乐观。
- 引入端到端 Agent loop 评估。
- 在 SFT 之后尝试 RLVR / GRPO / GSPO。
