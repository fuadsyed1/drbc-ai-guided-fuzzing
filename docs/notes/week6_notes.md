# Week 6 Notes: AI-Guided Fuzzer Implementation

## Goal

The goal of Week 6 was to implement the AI-guided fuzzer and compare it with the baseline random fuzzer.

The main task was to connect the fuzzing framework with a local Large Language Model, generate calculator fuzzing inputs, validate the generated inputs, execute them, log the results, and compare the AI-guided fuzzer against the random fuzzer.

## AI-Guided Fuzzer Implementation

The AI-guided fuzzer was implemented using a local Ollama model.

The selected model was:

* qwen3:1.7b

This model was chosen because it runs locally and supports reproducible experiments.

The AI-guided fuzzing pipeline includes:

* AI input generation
* AI output validation
* Input execution
* Result logging
* Summary generation
* Comparison with random fuzzing

The old AI fuzzer prototype used hardcoded inputs. During Week 6, it was replaced with a real AI generation pipeline.

## Files Created or Updated

The following files were created or updated:

* src/utils/ai_generator.py
* src/utils/ai_validator.py
* src/fuzzers/ai_fuzzer.py
* experiments/ai_guided_fuzzing/run_ai_fuzzer.py
* experiments/ai_guided_fuzzing/summarize_ai_results.py
* experiments/compare_results.py
* docs/notes/week6_notes.md

## Initial AI Experiment

The first working AI-guided experiment generated 20 inputs.

Result:

| Metric             | AI-Guided Fuzzer |
| ------------------ | ---------------: |
| Total Inputs       |               20 |
| Valid Inputs       |               18 |
| Crash/Error Inputs |                2 |

Observed error type:

* ZeroDivisionError

This result showed that the AI-guided fuzzer could generate meaningful calculator expressions. However, this was not a fair comparison because the random fuzzer had been tested with 100 inputs, while the AI-guided fuzzer had only been tested with 20 inputs.

## Failed Attempt: Generating 100 Inputs Directly

To make the comparison fair, the next attempt was to ask the model to generate 100 inputs in one request.

This approach failed because the local qwen3:1.7b model timed out after 120 seconds.

This showed that generating 100 inputs in a single model call was not reliable for the current local setup.

## Multi-Round Generation Attempt

To avoid the timeout problem, the AI fuzzer was changed to generate smaller batches.

Instead of asking for 100 inputs at once, the model was asked to generate 20 inputs per round.

This approach worked better, but it created a new problem.

One AI experiment generated:

| Metric             | AI-Guided Fuzzer |
| ------------------ | ---------------: |
| Total Inputs       |              121 |
| Valid Inputs       |               69 |
| Crash/Error Inputs |               52 |

Error types:

* ZeroDivisionError: 23
* SyntaxError: 29

This result was useful, but it was still not fair because the random fuzzer used 100 inputs while the AI-guided fuzzer used 121 inputs.

The AI-guided fuzzer had more chances to generate valid inputs and errors, so the comparison needed to be fixed.

## Final Fix: Fair Input Count

The AI-guided fuzzer was updated to stop after exactly 100 executed inputs.

A target input count was added:

```text
TARGET_INPUT_COUNT = 100
```

The experiment runner was changed so that it keeps generating inputs until it reaches 100 executed inputs. It also stops immediately once the target count is reached.

This fixed the fairness issue.

## Final Fair Comparison: Random vs AI-Guided Fuzzing

After fixing the AI-guided fuzzer, both fuzzers were evaluated using the same number of total inputs.

### Experimental Setup

* Random fuzzer inputs: 100
* AI-guided fuzzer inputs: 100
* Target program: calculator expression evaluator
* AI model: qwen3:1.7b through Ollama

### Results

| Metric                 |  Random Fuzzer | AI-Guided Fuzzer |
| ---------------------- | -------------: | ---------------: |
| Total Inputs           |            100 |              100 |
| Valid Inputs           |              8 |               61 |
| Crash/Error Inputs     |             92 |               39 |
| Average Execution Time | 0.00002734 sec |   0.00003274 sec |

### Random Fuzzer Error Types

* SyntaxError: 68
* ValueError: 13
* KeyError: 4
* IndentationError: 4
* ZeroDivisionError: 3

### AI-Guided Fuzzer Error Types

* ZeroDivisionError: 29
* SyntaxError: 10

### Analysis

The AI-guided fuzzer produced significantly more valid calculator expressions than the random fuzzer. Out of 100 inputs, the AI-guided fuzzer generated 61 valid inputs, while the random fuzzer generated only 8 valid inputs.

The random fuzzer produced more crash/error inputs and discovered a wider variety of error types. This shows that random fuzzing is useful for generating malformed inputs and exposing parser-level failures.

The AI-guided fuzzer was better at generating structured and meaningful arithmetic expressions. It also produced targeted edge cases such as division by zero. This suggests that AI-guided fuzzing can improve input validity and guide testing toward semantically meaningful cases.

The failed experiments were also useful. The 100-input direct generation attempt showed the limitation of the local model. The 121-input experiment showed why equal input counts are necessary for a fair comparison.

### Conclusion

Week 6 successfully implemented the AI-guided fuzzing pipeline.

For the final fair experiment, AI-guided fuzzing was more effective at generating valid test cases, while random fuzzing was more effective at producing diverse invalid inputs.

The final result suggests that both approaches have different strengths. Random fuzzing is useful for broad malformed-input exploration, while AI-guided fuzzing is useful for structured and targeted edge-case generation.

A future hybrid fuzzing approach could combine both strategies.
