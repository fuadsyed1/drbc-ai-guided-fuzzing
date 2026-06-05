# Background

## Fuzz Testing

Fuzz testing, or fuzzing, is an automated software testing technique that generates large numbers of inputs and executes a target program to identify crashes, unexpected behavior, and vulnerabilities. Fuzzing has become one of the most widely used methods for software security testing.

## Random Fuzzing

Random fuzzing generates inputs without any knowledge of the internal structure of the target program. Inputs are typically created using random mutations or random data generation. While simple and efficient, random fuzzing may spend significant time exploring uninteresting program paths.

## Coverage-Guided Fuzzing

Coverage-guided fuzzing improves upon random fuzzing by using code coverage information to guide input generation. Inputs that exercise new execution paths are retained and used to generate future test cases. AFL and AFLFast are well-known examples of coverage-guided fuzzers.

## Directed Fuzzing

Directed fuzzing focuses testing efforts toward specific locations in a program, such as recently modified code or known vulnerable functions. AFLGo is an example of a directed greybox fuzzer that guides execution toward target locations.

## AI-Guided Fuzzing

Recent advances in Large Language Models have enabled AI-guided fuzzing. Instead of relying solely on random mutations, language models can generate more structured and meaningful test inputs. Systems such as Fuzz4All and mGPTFuzz demonstrate how AI can assist fuzzing and improve bug discovery.