# AI-Guided Fuzzing Framework Architecture

```mermaid
flowchart TD
    A[Input Generation Layer] --> B1[Random Fuzzer]
    A --> B2[AI-Guided Fuzzer]

    B1 --> C1[Random Inputs]
    B2 --> C2[LLM Generated Inputs]

    C2 --> D[AI Output Validator]
    D --> E[Validated AI Inputs]

    C1 --> F[Execution Engine]
    E --> F

    F --> G[Calculator Target Program]
    G --> H[Result Logger]

    H --> I[JSONL Result Logs]
    I --> J[Summary Scripts]
    J --> K[Comparison Results]

    K --> L[Evaluation Metrics]
    L --> M[Research Analysis]