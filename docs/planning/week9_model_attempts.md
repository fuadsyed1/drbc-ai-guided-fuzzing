# Week 9 Model Attempt Notes

## Official completed models

- `qwen/qwen3.5-122b`
  - Completed 72 experiment groups.
  - Produced 36,000 target executions.
  - Included in the official Random-vs-AI comparison.

- `openai/gpt-oss-120b`
  - Completed 72 experiment groups.
  - Produced 36,000 target executions.
  - Included in the official Random-vs-AI comparison.

- `qwen/qwen3.6-35b`
  - Completed 72 experiment groups.
  - Produced 36,000 target executions.
  - One group initially failed during persistent MindRouter HTTP 502 responses.
  - The missing group completed successfully on retry.
  - Included in the official Random-vs-AI comparison.

- `google/gemma-4-31b`
  - Completed 72 experiment groups.
  - Produced 36,000 target executions.
  - Four groups initially failed because of malformed JSON responses,
    HTTP 502 errors, DNS failures, and connection interruptions.
  - All four missing groups completed successfully on retry.
  - Included in the official Random-vs-AI comparison.

## Incomplete and excluded model

- `Qwen/Qwen3-32B`
  - Initially required correction of the case-sensitive model identifier.
  - Completed 69 of 72 experiment groups.
  - Three groups remained incomplete after sustained MindRouter HTTP 502 failures.
  - Excluded from the equal-budget comparison.
  - Replaced by `qwen/qwen3.6-35b`.

## Reserve model

- `Nemotron-3-Super-120b`
  - Available through MindRouter.
  - Not tested during the official Week 9 experiment.
  - Retained as a possible future comparison model.
