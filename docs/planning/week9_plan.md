@'

\# Week 9 Plan: Full AI-Guided Fuzzing Experiments



\## Goal



Week 9 extends the Week 8 benchmark by replacing random input generation with AI-guided input generation.



Week 8 completed the full random baseline using 24 targets, five random fuzzing strategies, three trials, and 36,000 total executions. Week 9 will use the same 24-target benchmark suite so the AI-guided results can be compared fairly against the random baseline.



\## Main Objective



Run AI-guided fuzzing experiments across the existing 24 targets using multiple MindRouter models.



The AI fuzzer will use target metadata such as:



\- target name

\- difficulty

\- category

\- tokens

\- seed inputs

\- edge cases



The model will generate candidate fuzzing inputs. The framework will then validate, execute, log, and summarize those inputs using the same style as the Week 8 random baseline.



\## Selected AI Models



Initial MindRouter model set:



\- qwen/qwen3.5-122b

\- openai/gpt-oss-120b

\- qwen/qwen3-32b

\- google/gemma-4-31b



The first smoke test will use only:



\- qwen/qwen3.5-122b



After the smoke test works, the full experiment will run all selected models.



\## Experimental Design



Planned full experiment:



```text

24 targets × 4 AI models × 100 inputs × 3 trials = 28,800 AI-guided executions
