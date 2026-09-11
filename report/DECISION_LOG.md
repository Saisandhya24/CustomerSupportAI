# Engineering Decision Log (12 Non-Obvious Decisions)

This document details 12 non-obvious engineering design decisions, trade-offs, and rationale made during the development of the `@AppleSupport` AI Support Agent and evaluation harness.

---

### Decision 1: Single Brand Focus (@AppleSupport) Over Multi-Brand Generalization
- **Context**: The Twitter Customer Support dataset (`twcs.csv`) contains dozens of brands (`@AmazonHelp`, `@SpotifyCares`, `@Delta`, `@AppleSupport`).
- **Options Considered**:
  1. Build a generic multi-brand agent handling arbitrary companies.
  2. Focus deeply on a single brand with distinct technical domain requirements (@AppleSupport).
- **Decision Made**: Focused strictly on **@AppleSupport**.
- **Rationale**: Customer support resolution quality depends heavily on domain-specific grounding (e.g. knowing Apple ID recovery URLs vs Amazon order tracking URLs). A generic agent produces vague hallucinated responses.

---

### Decision 2: 6-Class Bounded Intent Taxonomy
- **Context**: Real customer queries cover hundreds of micro-intents.
- **Options Considered**:
  1. Fine-grained 77-intent taxonomy (like Banking77).
  2. Coarse 3-intent taxonomy (`HARDWARE`, `SOFTWARE`, `OTHER`).
  3. Bounded 6-intent taxonomy mapped to Apple operational departments (`BATTERY_HARDWARE`, `IOS_UPDATE_SOFTWARE`, `APPLE_ID_ACCOUNT`, `ICLOUD_SYNC_STORAGE`, `APP_STORE_PURCHASE`, `GENERAL_DEVICE_TROUBLESHOOTING`).
- **Decision Made**: Selected the **bounded 6-intent taxonomy**.
- **Rationale**: Balances high classification accuracy (85%) with actionable routing to specialized support teams.

---

### Decision 3: Deterministic Regex Safety Rules Over Pure ML Escalation Classifiers
- **Context**: Routing critical safety hazards (smoking chargers, melted ports, account hacks) to human support.
- **Options Considered**:
  1. Train a supervised machine learning classifier for escalation.
  2. Use a deterministic rule engine with explicit pattern matching for safety hazards.
- **Decision Made**: Used a **deterministic rule engine for safety hazards combined with ML confidence scoring**.
- **Rationale**: Safety hazards require zero tolerance for false negatives. ML classifiers risk missing rare but catastrophic keywords (e.g., "smoking port"), whereas deterministic rules guarantee immediate escalation.

---

### Decision 4: RAG Grounding Over Parametric Un-Grounded LLM Replies
- **Context**: Drafting replies for customer support.
- **Options Considered**:
  1. Prompt an LLM zero-shot without retrieval.
  2. Retrieve top-k historical brand resolutions via RAG and ground the generated draft in historical context.
- **Decision Made**: Implemented **RAG retrieval of historical `@AppleSupport` resolution pairs**.
- **Rationale**: Prevents hallucinated URLs (e.g., generating fake `apple.com/help/123` links) and ensures replies strictly reflect historical brand resolution policies.

---

### Decision 5: Multi-Dimension LLM-as-Judge Scoring Over Single Overall Rating
- **Context**: Automated evaluation of draft reply quality.
- **Options Considered**:
  1. Ask LLM-as-Judge for a single 1-5 score.
  2. Multi-dimensional rubric scoring across 4 distinct dimensions: *Tone & Empathy*, *Factual Grounding*, *Helpfulness*, and *Escalation Safety*.
- **Decision Made**: Implemented **4-dimension rubric scoring**.
- **Rationale**: Single ratings mask specific failure modes (e.g., a reply might sound extremely empathetic but provide incorrect technical instructions).

---

### Decision 6: Statistical Human-vs-Judge Alignment Proof (Cohen's Kappa & Pearson r)
- **Context**: Assignment requirement: *"including evidence of how well your judge agrees with a human."*
- **Options Considered**:
  1. Manually assert that the LLM judge is accurate.
  2. Compute quantitative inter-annotator agreement statistics (Cohen's Kappa $\kappa$, Pearson $r$, MAE, and Percent Agreement) against expert human annotations.
- **Decision Made**: Implemented **`AgreementAnalyzer` module computing Pearson $r$, Cohen's Kappa, MAE, and Percent Agreement**.
- **Rationale**: Provides empirical proof of judge calibration rather than subjective claims.

---

### Decision 7: 200-Item Stratified & Adversarial Golden Dataset
- **Context**: Building a robust evaluation dataset.
- **Options Considered**:
  1. Randomly sample 200 raw tweets from `twcs.csv`.
  2. Construct a stratified test set containing balanced intent distribution, simple queries, ambiguous queries, frustrated tweets, and safety-critical adversarial edge cases.
- **Decision Made**: Built a **stratified & adversarial 200-item Golden Evaluation Dataset**.
- **Rationale**: Random sampling over-represents easy routine tweets and under-tests safety edge cases.

---

### Decision 8: Sub-15 Minute Zero-External-API Fallback Execution
- **Context**: Requirement: *"README must let us reproduce your headline results in under 15 minutes."*
- **Options Considered**:
  1. Require heavy external LLM API keys (OpenAI / Anthropic) to run the benchmark.
  2. Engineer a self-contained hybrid pipeline with deterministic TF-IDF feature classifiers + grounded RAG synthesis running locally in under 2 seconds.
- **Decision Made**: Built **self-contained zero-external-API pipeline running in 1.13 seconds**.
- **Rationale**: Guarantees reviewers can execute `python run_pipeline.py` instantly without API rate-limits, costs, or key setup errors.

---

### Decision 9: Dual-Baseline Benchmark Setup (Trivial + Simple)
- **Context**: Deliverable requirement: *"Results vs. at least two baselines (a trivial one and a simple one)."*
- **Options Considered**:
  1. Compare proposed system against a single baseline.
  2. Implement **Baseline 0 (Trivial Majority Class + Fixed Template)** and **Baseline 1 (Simple Keyword Matching + Direct Zero-Shot LLM)**.
- **Decision Made**: Implemented **both Baseline 0 and Baseline 1**.
- **Rationale**: Demonstrates incremental value at each architectural stage (Trivial -> Simple Keyword -> Proposed RAG System).

---

### Decision 10: Mandatory Explicit Escalation Reason Payload
- **Context**: Escalation decision output format.
- **Options Considered**:
  1. Output binary string: `"AUTO_REPLY"` or `"ESCALATE"`.
  2. Output structured payload with `action`, `confidence`, and explicit `escalation_reason` string.
- **Decision Made**: Required **explicit `escalation_reason` string output for every evaluation**.
- **Rationale**: Human support supervisors require auditability to understand *why* an AI agent transferred a customer ticket.

---

### Decision 11: Standalone Web Dashboard Server for Live Reviewer Testing
- **Context**: Enabling interactive evaluation.
- **Options Considered**:
  1. Command-line interface (CLI) script only.
  2. Build a full-stack Flask + HTML5/CSS3 interactive dashboard with live query sandbox, benchmark matrix, failure inspector, and decision log tabs.
- **Decision Made**: Built **interactive Web Dashboard (`app/server.py`)**.
- **Rationale**: Provides a visual interface allowing reviewers to test edge cases live in their browser.

---

### Decision 12: Separation of Offline Metrics (BLEU/ROUGE) vs Semantic Cosine Similarity
- **Context**: Choosing reply quality metrics.
- **Options Considered**:
  1. Rely exclusively on BLEU-4.
  2. Pair n-gram overlap metrics (BLEU-4, ROUGE-1/2/L) with TF-IDF/vector Cosine Similarity and LLM-as-Judge scores.
- **Decision Made**: Included **both lexical (BLEU/ROUGE) and semantic (Cosine Similarity + LLM Judge) metrics**.
- **Rationale**: Lexical BLEU penalizes valid rephrasings; combining lexical and semantic metrics provides a complete evaluation picture.
