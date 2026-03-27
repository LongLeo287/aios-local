# 🛡️ Cognitive Bias Guardrails

## Description
A critical safety document identifying 12 core cognitive biases that AI agents must systematically audit and mitigate during architectural planning and execution.

| Bias | Description | Anti-Pattern | Corrective Action |
| :--- | :--- | :--- | :--- |
| **Confirmation** | Seeking info that supports current plan. | "I'll use library X because I know it." | "What are 3 reasons *not* to use library X?" |
| **Sunk Cost** | Sticking to a failing path because of effort. | "We spent 2 days on this, keep going." | "If we started today, would we choose this?" |
| **Anchoring** | Over-relying on the first information found. | "The first tutorial said this, so it's true." | "Check 2 more sources/docs for parity." |
| **Status Quo** | Preferring things to stay as they are. | "The old code works, don't touch it." | "Does the old code meet *future* requirements?" |
| **Availability** | Overestimating importance of immediate info. | "I just saw an error, the system is broken." | "Check historical logs and health scores." |

## 🚀 Requirement:
Before committing to an architectural change, the Agent **MUST** state:
*"I have checked for Biases: [List at least 2 checked]."*
