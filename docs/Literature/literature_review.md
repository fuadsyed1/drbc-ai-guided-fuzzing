# Literature Review

## Paper 1: AFLFast

**Authors:** Marcel Böhme, Van-Thuan Pham, Abhik Roychoudhury

**Year:** 2016

**Research Problem:**
Traditional greybox fuzzers spend too much time exploring common execution paths and may fail to efficiently reach deeper program states where bugs exist.

**Method:**
The authors model coverage-based greybox fuzzing as a Markov chain and introduce new power schedules that assign more fuzzing effort to low-frequency execution paths.

**Key Results:**
AFLFast discovered multiple previously unknown vulnerabilities and exposed several CVEs significantly faster than AFL. The study showed that focusing on rarely executed paths improves fuzzing efficiency.

**Limitations:**
The approach improves efficiency but still relies on mutation-based fuzzing and does not use semantic understanding of inputs.

**Relevance to This Project:**
This paper provides the foundation for understanding how fuzzing strategies can be improved beyond simple random input generation. It serves as a useful baseline when comparing traditional fuzzing approaches with AI-guided fuzzing.

---

## Paper 2: AFLGo

**Authors:** Marcel Böhme, Van-Thuan Pham, Manh-Dung Nguyen, Abhik Roychoudhury

**Year:** 2017

**Research Problem:**
Standard greybox fuzzers are not designed to focus on specific regions of code such as recently modified functions, vulnerable locations, or crash locations.

**Method:**
The authors introduce Directed Greybox Fuzzing (DGF), which computes distances to target locations and prioritizes inputs that move execution closer to those targets.

**Key Results:**
AFLGo reached target locations faster than traditional fuzzers and discovered multiple vulnerabilities in widely used software projects.

**Limitations:**
The method requires predefined target locations and is not intended for general exploration of unknown vulnerabilities.

**Relevance to This Project:**
This paper demonstrates the value of guidance during fuzzing. AI-guided fuzzing follows a similar idea by using intelligent input generation instead of purely random mutations.

---

## Paper 3: Dissecting AFL

**Authors:** Andrea Fioraldi, Alessandro Mantovani, Dominik Maier, Davide Balzarotti

**Year:** 2023

**Research Problem:**
Many fuzzers are based on AFL, but the effectiveness of AFL's internal design choices has not been thoroughly studied.

**Method:**
The authors evaluated AFL using the FuzzBench platform and performed experiments on scheduling strategies, mutation methods, coverage feedback, and other design components.

**Key Results:**
The study identified which AFL components contribute most to bug discovery and coverage. Some commonly used features were shown to be more important than others.

**Limitations:**
The paper focuses on AFL and its variants rather than comparing AFL with AI-based fuzzing approaches.

**Relevance to This Project:**
This paper helps identify appropriate evaluation metrics and experimental practices for comparing fuzzing techniques.

---

## Paper 4: Fuzz4All

**Authors:** Chunqiu Steven Xia, Matteo Paltenghi, Jia Le Tian, Michael Pradel, Lingming Zhang

**Year:** 2024

**Research Problem:**
Traditional fuzzers often require language-specific rules and struggle to adapt to new programming languages or language features.

**Method:**
Fuzz4All uses Large Language Models as a universal input generation and mutation engine. It introduces automatic prompt generation and an LLM-powered fuzzing loop.

**Key Results:**
The system achieved higher code coverage than several specialized fuzzers and discovered numerous previously unknown bugs across multiple programming languages and systems.

**Limitations:**
The effectiveness of the approach depends on the capabilities of the underlying language model and may require significant computational resources.

**Relevance to This Project:**
This paper is directly related to the research goal because it demonstrates how LLMs can be used to guide fuzzing and improve bug discovery.

---

## Paper 5: mGPTFuzz

**Authors:** Xiaoyue Ma, Lannan Luo, Qiang Zeng

**Year:** 2024

**Research Problem:**
Testing Matter IoT devices is difficult because of large specifications, complex device states, and limited visibility into device internals.

**Method:**
The authors use a Large Language Model to extract testing knowledge from Matter specifications and generate stateful fuzzing inputs for IoT devices.

**Key Results:**
mGPTFuzz discovered 147 new bugs, including multiple CVEs, significantly outperforming existing IoT fuzzing approaches.

**Limitations:**
The approach focuses specifically on Matter IoT devices and may not directly generalize to all software systems.

**Relevance to This Project:**
This paper provides strong evidence that AI-assisted fuzzing can outperform traditional approaches by generating more meaningful test inputs and exploring complex behaviors.
