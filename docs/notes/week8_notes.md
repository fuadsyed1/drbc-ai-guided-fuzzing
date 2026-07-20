# Week 8 Notes: Full Random Baseline Evaluation

## Goal

This week I built the final random fuzzing baseline for the project. The earlier experiments only used the calculator target, which was too narrow for the final paper. To make the baseline stronger and more realistic, I expanded the benchmark to multiple target programs and multiple random fuzzing strategies.

The goal was to measure how far random fuzzing can go before comparing it with AI-guided fuzzing.

## Benchmark Design

I created a benchmark suite with 24 target programs divided into three difficulty levels:

- 8 easy targets
- 8 moderate targets
- 8 hard targets

The targets include validators, parsers, protocol-like inputs, command-like inputs, arithmetic expressions, template rendering, boolean expressions, and XML-like structures.

This gives the project a broader evaluation than using only a calculator program.

## Random Fuzzing Strategies

I implemented five random fuzzing strategies:

1. Basic character random fuzzing
2. Token-aware random fuzzing
3. Edge-case seed random fuzzing
4. Mutation-based random fuzzing
5. Coverage-guided random fuzzing

Each strategy was tested on every target.

## Experiment Setup

The final random baseline used:

- 24 targets
- 5 random fuzzing strategies
- 100 inputs per target/strategy/trial
- 3 trials

Total executions:

```text
24 × 5 × 100 × 3 = 36,000 executions