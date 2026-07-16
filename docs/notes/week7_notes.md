# Week 7 Notes: Pilot Experiments and Paper Drafting

## Goal

The goal of Week 7 is to begin pilot experiments using the completed random fuzzing and AI-guided fuzzing framework.

After completing the Week 6 fair comparison with 100 inputs for each fuzzer, I started Week 7 by running a smaller 50 vs 50 pilot experiment. The purpose of this pilot experiment was to check whether the workflow is stable, whether result logging works correctly, and whether the summary script can compare both fuzzers automatically.

## Pilot Experiment Setup

For the Week 7 pilot experiment, I used the same calculator expression evaluator target.

The setup was:

* Random fuzzer inputs: 50
* AI-guided fuzzer inputs: 50
* Target program: calculator expression evaluator
* AI model: qwen3:1.7b through Ollama
* Output format: JSONL result logs
* Summary format: JSON summary file

The pilot results were saved separately from the Week 6 results so that the final Week 6 100 vs 100 comparison would not be overwritten.

## Files Created or Updated

The following files were created or updated during this step:

* experiments/week7_pilot/run_pilot_experiment.py
* experiments/week7_pilot/summarize_week7_pilot.py
* results/logs/week7_random_pilot_results.jsonl
* results/logs/week7_ai_pilot_results.jsonl
* results/logs/week7_pilot_summary.json
* docs/notes/week7_notes.md

## Pilot Experiment Result

The Week 7 pilot experiment completed successfully.

Both fuzzers were evaluated using 50 total inputs.

| Metric                 |   Random Pilot |       AI Pilot |
| ---------------------- | -------------: | -------------: |
| Total Inputs           |             50 |             50 |
| Valid Inputs           |              3 |             42 |
| Crash/Error Inputs     |             47 |              8 |
| Unique Inputs          |             47 |             50 |
| Duplicate Inputs       |              3 |              0 |
| Average Execution Time | 0.00003119 sec | 0.00002818 sec |

## Random Pilot Error Types

The random fuzzer produced the following error types:

* SyntaxError: 34
* ValueError: 7
* ZeroDivisionError: 4
* KeyError: 1
* IndentationError: 1

## AI Pilot Error Types

The AI-guided fuzzer produced the following error type:

* ZeroDivisionError: 8

## Analysis

The Week 7 pilot experiment shows a similar pattern to the Week 6 fair comparison.

The AI-guided fuzzer generated far more valid calculator expressions than the random fuzzer. Out of 50 inputs, the AI-guided fuzzer generated 42 valid inputs, while the random fuzzer generated only 3 valid inputs.

The random fuzzer produced more crash/error inputs and a wider variety of error types. This shows that random fuzzing is useful for generating malformed inputs and exposing parser-level failures.

The AI-guided fuzzer produced fewer errors, but its errors were more targeted. In this pilot run, all AI-guided fuzzer errors were ZeroDivisionError cases.

The random fuzzer also produced duplicate inputs. It executed 50 total inputs, but only 47 were unique. The AI-guided fuzzer produced 50 unique inputs with no duplicates.

## Workflow Debugging

During this step, I found an issue in the first version of the Week 7 summary script.

The first summary script incorrectly counted all inputs as crash/error inputs. It reported 0 valid inputs for both fuzzers even though the actual result files showed successful executions.

The issue happened because the script was not reading the result log format correctly. I fixed the summary script so it correctly detects valid executions, crash/error inputs, execution time, unique inputs, duplicate inputs, and error types.

After fixing the script, the corrected summary showed the expected result:

* Random pilot: 3 valid inputs and 47 crash/error inputs
* AI pilot: 42 valid inputs and 8 crash/error inputs

This debugging step was important because it confirmed that the analysis script must match the actual JSONL logging format.

## Conclusion

The Week 7 pilot experiment successfully tested the experimental workflow using a smaller 50 vs 50 setup.

The result supports the same observation from Week 6: AI-guided fuzzing is better at producing valid and structured calculator inputs, while random fuzzing is better at producing malformed inputs and diverse parser-level errors.

This pilot also helped confirm that separate result files are useful for preserving different experiment stages. Week 6 results remain separate from Week 7 pilot results, which prevents accidental overwriting and keeps the research process organized.

## Next Steps

The next steps are:

* Add a paper draft section for System Architecture.
* Add a paper draft section for Implementation Details.
* Create or update an architecture diagram for the fuzzing framework.
* Continue refining evaluation metrics such as total inputs, unique inputs, valid inputs, crash/error inputs, unique error types, and execution time.

## Additional Week 7 Deliverables Completed

After completing the pilot experiment and fixing the Week 7 summary script, I also completed the remaining Week 7 deliverables.

I created a system architecture figure to show how the framework connects input generation, AI validation, execution, logging, summary generation, and comparison analysis.

I also drafted two paper sections:

- System Architecture
- Implementation Details

These drafts describe the framework structure, the role of each component, and how the random and AI-guided fuzzers are evaluated using the same pipeline.

## Completed Week 7 Deliverables

- Pilot experiment results
- Debugged summary workflow
- Refined evaluation metrics
- Architecture figure
- System Architecture draft
- Implementation Details draft