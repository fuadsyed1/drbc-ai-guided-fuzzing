# Week 8 Plan: Full Random Fuzzing Experiments

## Main Goal

The goal of Week 8 is to create the final random fuzzing baseline for the paper.

Until now, the project tested random fuzzing and AI-guided fuzzing mainly on the calculator target. That was useful for early development, but it is not enough for a strong final research paper.

For Week 8, I will expand the experiment from one target program to a full benchmark suite.

The final Week 8 setup will include:

* 24 target programs
* 5 random fuzzing strategies
* 100 inputs per target per fuzzer
* 3 trials per experiment

This gives the final random baseline:

```text
24 targets × 5 fuzzers × 100 inputs × 3 trials = 36,000 executions
```

This will make the random fuzzing baseline stronger, more diverse, and more suitable for the final paper.

---

## Step 1: Create the Target Program Suite

The first step is to create 24 target programs.

These programs will not be large applications. Instead, they will be small input-processing programs designed for fuzzing experiments.

Each target program should:

* Accept one string input
* Process, parse, or validate the input
* Return a result for valid input
* Produce errors or exceptions for malformed input
* Be easy to run automatically
* Work with all random fuzzing strategies

Each target will use a standard function format:

```python
def process_input(input_string):
    ...
```

This makes the experiment runner simple because every target can be executed in the same way.

---

## Step 2: Target Difficulty Groups

The 24 target programs will be divided into three difficulty levels:

* Easy
* Moderate
* Hard

This allows the paper to compare how random fuzzing behaves on simple targets versus structured and grammar-like targets.

---

## Easy Targets

Easy targets are simple validation or parsing programs.

| No. | Target Program          | What It Tests                     |
| --: | ----------------------- | --------------------------------- |
|   1 | calculator.py           | Arithmetic expressions            |
|   2 | email_validator.py      | Email format validation           |
|   3 | password_checker.py     | Password policy rules             |
|   4 | date_parser.py          | Date formats and invalid dates    |
|   5 | phone_validator.py      | Phone number formats              |
|   6 | zip_code_validator.py   | ZIP/postal code formats           |
|   7 | username_validator.py   | Username rules                    |
|   8 | color_code_validator.py | Hex color codes such as `#FFAA00` |

The calculator target is kept as the prerequisite easy target because it was used in earlier weeks.

---

## Moderate Targets

Moderate targets use more structured input formats.

| No. | Target Program          | What It Tests                   |
| --: | ----------------------- | ------------------------------- |
|   9 | csv_parser.py           | Comma-separated values          |
|  10 | json_parser.py          | JSON objects                    |
|  11 | url_parser.py           | URL structure                   |
|  12 | config_parser.py        | `key=value` configuration input |
|  13 | query_string_parser.py  | URL query string format         |
|  14 | log_line_parser.py      | Structured log lines            |
|  15 | markdown_link_parser.py | Markdown link syntax            |
|  16 | file_path_parser.py     | File path patterns              |

These targets are important because many real applications process structured text input.

---

## Hard Targets

Hard targets are grammar-like, protocol-like, or multi-step parsers.

| No. | Target Program               | What It Tests                          |
| --: | ---------------------------- | -------------------------------------- |
|  17 | sql_where_parser.py          | SQL-style WHERE conditions             |
|  18 | command_parser.py            | Commands, flags, and arguments         |
|  19 | template_renderer.py         | Placeholder syntax                     |
|  20 | http_request_parser.py       | HTTP request format                    |
|  21 | mini_protocol_parser.py      | Message protocol parsing               |
|  22 | arithmetic_script_parser.py  | Multi-step arithmetic scripts          |
|  23 | boolean_expression_parser.py | Boolean expressions using AND, OR, NOT |
|  24 | xml_like_parser.py           | Tag matching and nesting               |

These targets make the benchmark suite stronger because they represent language-like and protocol-like inputs.

---

## Step 3: Create the Target Registry

After creating the target suite, I will create a target registry.

The target registry will describe every target program in one place.

The registry should include:

* Target name
* Difficulty level
* Target category
* Module path
* Function name
* Valid seed examples
* Target-specific tokens
* Edge cases

Example registry entry:

```python
{
    "name": "email_validator",
    "difficulty": "easy",
    "category": "format_validator",
    "module": "src.targets.benchmark_suite.email_validator",
    "function": "process_input",
    "tokens": ["@", ".", "com", "edu", "org"],
    "seeds": ["user@example.com", "student@university.edu"],
    "edge_cases": ["", "user@", "@domain.com", "user@@example.com"]
}
```

The registry is important because the fuzzers and experiment runner will use it to automatically run experiments across all 24 targets.

---

## Step 4: Implement 5 Random Fuzzing Strategies

For the final paper, I will not use only one random fuzzer.

A single random fuzzer would create a weak baseline. Instead, Week 8 will compare five different random fuzzing strategies.

The five random fuzzers are:

1. Basic Character Random Fuzzer
2. Token-Aware Random Fuzzer
3. Edge-Case Seed Random Fuzzer
4. Mutation-Based Random Fuzzer
5. Coverage-Guided Random Fuzzer

This gives a stronger baseline because it includes both simple random generation and stronger AFL-style ideas such as mutation and coverage guidance.

---

## Fuzzer 1: Basic Character Random Fuzzer

The Basic Character Random Fuzzer is the simplest baseline.

It generates strings by randomly selecting characters from a general character set.

Example characters include:

```text
letters, numbers, symbols, operators, brackets, punctuation
```

Example generated inputs may look like:

```text
a))9+/*x
77//abc
{{{
@3#xY
```

Purpose:

This fuzzer represents the weakest pure random baseline. It helps show how unguided random input generation performs across the target suite.

---

## Fuzzer 2: Token-Aware Random Fuzzer

The Token-Aware Random Fuzzer uses target-specific tokens.

Instead of choosing only random characters, it uses tokens that are meaningful for each target.

Examples:

```text
Email target: @, ., com, edu
JSON target: {, }, :, ", ,
SQL target: AND, OR, =, >, <
HTTP target: GET, POST, /, HTTP/1.1
```

Purpose:

This fuzzer tests whether target-aware random token generation performs better than pure character random generation.

It is still random, but it has better vocabulary for each target.

---

## Fuzzer 3: Edge-Case Seed Random Fuzzer

The Edge-Case Seed Random Fuzzer uses known edge cases.

It randomly selects edge cases from the target registry and may repeat, combine, or slightly modify them.

Example edge cases include:

```text
empty string
single space
very long string
missing symbols
division by zero
invalid dates
unclosed braces
duplicate separators
```

Purpose:

This fuzzer tests whether known boundary cases and malformed examples expose more failures than pure random generation.

---

## Fuzzer 4: Mutation-Based Random Fuzzer

The Mutation-Based Random Fuzzer starts from valid seed inputs and randomly mutates them.

Example valid seed:

```text
user@example.com
```

Possible mutations:

```text
user@@example.com
userexample.com
user@example
user@example..com
```

Mutation operations may include:

* Deleting a character
* Inserting a random character
* Replacing a character
* Duplicating a substring
* Swapping characters
* Removing required symbols

Purpose:

This is closer to real fuzzing practice because many fuzzers mutate existing valid inputs.

This fuzzer should produce a mixture of valid, near-valid, and invalid inputs.

---

## Fuzzer 5: Coverage-Guided Random Fuzzer

The Coverage-Guided Random Fuzzer is the strongest random baseline.

It mutates inputs and keeps inputs that increase code coverage.

Simplified logic:

```text
Generate or mutate input
Run target program
Measure coverage
If coverage improves, keep input as a new seed
Repeat
```

Purpose:

This gives the project a simplified AFL-style baseline.

It is important for the final paper because it shows that AI-guided fuzzing is not being compared only against a weak random fuzzer.

---

## Step 5: Create the Week 8 Experiment Runner

The main Week 8 experiment runner will be:

```text
experiments/week8_random_baseline/run_week8_random_experiments.py
```

The runner will execute:

```text
for each target:
    for each random fuzzer:
        for each trial:
            generate 100 inputs
            execute inputs
            save results
```

This will create the full 36,000-execution random baseline.

The result files should be saved separately by target, fuzzer, and trial.

Example output paths:

```text
results/week8/random_baseline/email_validator/basic_random_trial1.jsonl
results/week8/random_baseline/email_validator/token_random_trial1.jsonl
results/week8/random_baseline/email_validator/mutation_random_trial1.jsonl
results/week8/random_baseline/json_parser/basic_random_trial1.jsonl
```

This keeps the result files organized and easy to inspect.

---

## Step 6: Collect Metrics

For every target, fuzzer, and trial, the experiment should collect:

* Total inputs
* Valid inputs
* Crash/error inputs
* Unique inputs
* Duplicate inputs
* Unique error types
* Error type counts
* Average execution time
* Coverage percentage
* Target difficulty
* Target category
* Fuzzer type

These metrics are important for both the Week 8 report and the final paper.

---

## Step 7: Create Summary Scripts

After running the experiments, I will create a summary script:

```text
experiments/week8_random_baseline/summarize_week8_random_results.py
```

This script will read all Week 8 random baseline result files and produce:

```text
results/week8/random_baseline/week8_random_summary.json
results/week8/random_baseline/week8_random_summary.csv
```

The JSON file will preserve structured experiment data.

The CSV file will be used for tables, charts, and paper results.

---

## Step 8: Create Data Tables

The Week 8 summary should support multiple paper-ready tables.

### Table 1: Result by Difficulty

This table will compare random fuzzing results across:

* Easy targets
* Moderate targets
* Hard targets

### Table 2: Result by Fuzzer Type

This table will compare:

* Basic character random fuzzer
* Token-aware random fuzzer
* Edge-case seed random fuzzer
* Mutation-based random fuzzer
* Coverage-guided random fuzzer

### Table 3: Result by Target Program

This table will show the result for all 24 target programs individually.

### Table 4: Error Type Distribution

This table will show what kinds of errors each fuzzer discovered.

Example error categories:

* SyntaxError
* ValueError
* KeyError
* ZeroDivisionError
* Parser errors
* Validation errors
* Format errors

---

## Step 9: Write Week 8 Notes

After the experiments are complete, I will write:

```text
docs/notes/week8_notes.md
```

The Week 8 notes should include:

* Week 8 goal
* Target suite design
* Random fuzzing strategies
* Experiment setup
* Number of executions
* Result summary
* Data tables
* Main findings
* Limitations
* Next steps

---

## Step 10: Update Paper Draft Sections

After the Week 8 results are ready, I will update the paper/report writing.

The following files should be updated:

```text
reports/methodology.md
reports/system_architecture.md
reports/implementation_details.md
```

The updates should include:

* 24-target benchmark suite
* Easy, moderate, and hard target categories
* 5 random fuzzing strategies
* 36,000 total random fuzzing executions
* Evaluation metrics
* Random baseline result tables

This will make the final paper much stronger.

---

## Step 11: Commit Everything Together

The Week 8 commit should happen only after all deliverables are complete.

The commit should include:

* 24 target programs
* Target registry
* 5 random fuzzing strategies
* Week 8 experiment runner
* Week 8 summary script
* Result logs
* Summary JSON
* Summary CSV
* Data tables
* Week 8 notes
* Updated report sections

Commit message:

```powershell
git commit -m "Add Week 8 full random fuzzing baseline experiments"
```

---

## Week 8 Deliverables

By the end of Week 8, the completed deliverables should be:

* 24 target programs
* Target registry
* 5 random fuzzing strategies
* Full random baseline experiment runner
* 36,000 random fuzzing executions
* Result logs
* Summary JSON
* Summary CSV
* Data tables
* Week 8 notes
* Updated methodology/report writing

---