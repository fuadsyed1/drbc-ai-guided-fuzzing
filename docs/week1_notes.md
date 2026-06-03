# Week 1 Notes

## What is Fuzz Testing?
Fuzz testing is a software testing method where a program is tested using many different inputs. Some inputs are normal, and some are random or unexpected. The goal is to find crashes, bugs, or security problems.

## What is Random Fuzzing?
Random fuzzing generates inputs without much knowledge of the program. It is simple and fast, but many inputs may be useless because they do not follow the expected format.

## What is AI-Guided Fuzzing?
AI-guided fuzzing uses a language model to generate more meaningful test inputs. Instead of only creating random data, the AI can try to create inputs that look closer to real program input.

## Why Compare Them?
Random fuzzing is simple and common, but AI-guided fuzzing may find bugs faster if it creates smarter inputs. This project will compare both methods using the same target program and the same evaluation metrics.

## Possible Metrics
- Number of crashes found
- Code coverage
- Number of inputs tested
- Time taken
- Unique bugs discovered
