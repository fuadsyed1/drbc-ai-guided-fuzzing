# AI Output Validation Rules

## Goal

The goal of this step is to clean and validate outputs produced by the language model before sending them to the fuzzing execution pipeline.

## Problem

Language models may generate extra text, explanations, numbering, markdown formatting, or duplicate inputs. These outputs must be cleaned before execution.

## Cleaning Rules

The AI output cleaner should:

* Remove blank lines
* Remove numbered list markers
* Remove bullet markers
* Remove markdown formatting
* Remove explanations
* Strip extra spaces
* Remove duplicate inputs

## Input Filtering Rules

Generated inputs should be filtered using simple rules:

* Keep only short calculator-like strings
* Limit maximum input length
* Keep expressions containing calculator-related characters
* Remove lines that look like sentences
* Remove lines that are clearly explanations

## Allowed Characters

The initial calculator target supports inputs containing:

```text
0123456789+-*/() 
