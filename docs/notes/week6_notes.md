## Final Fair Comparison: Random vs AI-Guided Fuzzing

After fixing the AI-guided fuzzer, both fuzzers were evaluated using the same number of total inputs.

### Experimental Setup

- Random fuzzer inputs: 100
- AI-guided fuzzer inputs: 100
- Target program: calculator expression evaluator
- AI model: qwen3:1.7b through Ollama

### Results

| Metric | Random Fuzzer | AI-Guided Fuzzer |
|---|---:|---:|
| Total Inputs | 100 | 100 |
| Valid Inputs | 8 | 61 |
| Crash/Error Inputs | 92 | 39 |
| Average Execution Time | 0.00002734 sec | 0.00003274 sec |

### Random Fuzzer Error Types

- SyntaxError: 68
- ValueError: 13
- KeyError: 4
- IndentationError: 4
- ZeroDivisionError: 3

### AI-Guided Fuzzer Error Types

- ZeroDivisionError: 29
- SyntaxError: 10

### Analysis

The AI-guided fuzzer produced significantly more valid calculator expressions than the random fuzzer. Out of 100 inputs, the AI-guided fuzzer generated 61 valid inputs, while the random fuzzer generated only 8 valid inputs.

The random fuzzer produced more crash/error inputs and discovered a wider variety of error types. This shows that random fuzzing is useful for generating malformed inputs and exposing parser-level failures.

The AI-guided fuzzer was better at generating structured and meaningful arithmetic expressions. It also produced targeted edge cases such as division by zero. This suggests that AI-guided fuzzing can improve input validity and guide testing toward semantically meaningful cases.

### Conclusion

For this experiment, AI-guided fuzzing was more effective at generating valid test cases, while random fuzzing was more effective at producing diverse invalid inputs. A future hybrid fuzzing approach could combine both strategies: random fuzzing for broad malformed input exploration and AI-guided fuzzing for structured edge-case generation.