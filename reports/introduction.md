# Introduction

Software bugs and vulnerabilities remain a major challenge in modern software systems. Detecting these issues early is important for improving software reliability and security.

Fuzz testing has become one of the most successful automated techniques for discovering software defects. Traditional fuzzing approaches generate large numbers of test inputs and execute a target program to identify crashes, unexpected behavior, and vulnerabilities.

Over the years, researchers have developed more advanced fuzzing techniques such as coverage-guided fuzzing and directed fuzzing to improve bug discovery efficiency. Tools such as AFL, AFLFast, and AFLGo have demonstrated significant success in discovering vulnerabilities in real-world software systems.

Recent advances in Large Language Models (LLMs) have introduced new opportunities for software testing. Instead of relying solely on random mutations, LLMs can generate more meaningful and structured inputs that may explore program behaviors more effectively.

This research investigates the use of AI-guided fuzzing and compares it with traditional fuzzing approaches. The goal is to evaluate whether language-model-assisted fuzzing can improve bug discovery, code coverage, and testing efficiency.