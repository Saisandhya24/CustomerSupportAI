# Golden Evaluation Dataset: Sampling and Labeling Methodology

## 1. Executive Summary
The Golden Evaluation Dataset consists of **200 hand-curated and annotated Twitter customer support queries** directed at **@AppleSupport**. It serves as an un-leaked, gold-standard benchmark to evaluate intent classification accuracy, retrieval grounding, escalation routing precision, and draft reply quality.

---

## 2. Sampling Strategy
To capture real-world operational complexity and avoid trivial benchmark inflation, we applied a **Stratified & Adversarial Sampling Methodology**:

1. **Stratified Intent Balance (33.3% per dominant category clusters)**:
   - Queries were sampled across all 6 core brand intents (`BATTERY_HARDWARE`, `IOS_UPDATE_SOFTWARE`, `APPLE_ID_ACCOUNT`, `ICLOUD_SYNC_STORAGE`, `APP_STORE_PURCHASE`, `GENERAL_DEVICE_TROUBLESHOOTING`).
2. **Difficulty Stratification**:
   - **Simple (50%)**: Direct single-topic queries with explicit keywords (e.g., "forgot Apple ID password").
   - **Ambiguous (15%)**: Short or underspecified queries (e.g., "Wi-Fi greyed out", "storage full").
   - **Frustrated / Churn Risk (15%)**: Emotionally charged, angry, or threatening tweets (e.g., "ruined my phone", "switching to Samsung").
   - **Adversarial / Safety Critical (10%)**: Account compromise, physical battery overheating/smoke, or child unauthorized billing.
   - **Multi-Intent (10%)**: Tweets combining multiple issues (e.g., "battery drain AND iOS update freeze").

---

## 3. Annotation Schema & Guidelines
Each sample was annotated according to strict operational rules:

| Field | Description | Annotation Constraint |
|---|---|---|
| `id` | Unique sample identifier | Format: `EVAL_[CATEGORY]_[NUM]` |
| `tweet_text` | Customer raw Twitter query | Original text preserving typos, emojis, and handle tagging |
| `ground_truth_intent` | Labeled intent class | Exactly one of the 6 defined taxonomy categories |
| `ground_truth_action` | Action decision | `AUTO_REPLY` (safe for automated resolution) or `ESCALATE` (requires human agent) |
| `ground_truth_escalation_reason` | Explicit rationale | Stated operational reason for escalation (e.g., safety hazard, PII verification, financial refund) |
| `reference_resolution` | Gold standard resolution | Ground truth resolution grounded in official Apple Customer Care guidelines |
| `human_quality_score` | Expert human rating | Benchmark score (1.0 to 5.0 scale) used to validate LLM-as-Judge alignment |

---

## 4. Quality Control & Agreement Verification
- **Dual Verification**: All 200 items underwent strict verification against official Apple support knowledge bases (`support.apple.com`).
- **Zero Data Leakage**: None of the 200 golden evaluation queries overlap with the RAG historical resolution index (`twcs_apple_sample.json`).
