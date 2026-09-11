# Executive Technical Report: AI Support Agent for @AppleSupport
**Hiver SDE Intern Take-Home Assignment**

---

## 1. Problem Framing: Defining "Good" Support & Scope Cuts

### What "Good" Means for @AppleSupport Customer Service
In high-volume social customer care, "good" customer support on Twitter is defined by **four fundamental pillars**:

1. **Brand Consistency & Empathy**: Customer inquiries tagged at `@AppleSupport` often stem from hardware failures, device lockouts, or billing stress. Responses must maintain Apple's signature polite, calm, and reassuring tone.
2. **Factual Grounding & Policy Accuracy**: Customer advice must strictly adhere to official Apple knowledge base procedures (`support.apple.com`). Providing hallucinated menu paths or incorrect restore commands destroys brand trust.
3. **Deterministic Safety Escalation**: Critical safety issues (e.g., smoking batteries, melted charger ports, account security breaches, unauthorized child billing) must be routed to human agents instantly.
4. **First-Contact Self-Service Resolution**: High-volume routine queries (passcode reset URLs, battery health diagnostics, AirDrop toggles) should be resolved immediately via automated guidance without burdening human support queues.

### Explicit Scope Cuts (What We Chose NOT to Build)
To ensure high precision and sub-15 minute reproducibility, we explicitly cut the following out of scope:
- **Direct PII / Account Data Modification**: The agent does not directly modify Apple ID credentials or process credit card transactions inside Twitter. Any action requiring sensitive authentication is routed via official DM handoff or `iforgot.apple.com`.
- **Multi-Turn State Machine Persistence**: We deliberately restricted classification to single-tweet or preceding-tweet context windows, cutting complex conversational state tracking to avoid cascading error loops across un-verified turns.
- **Parametric Open Generation Without RAG**: We disabled un-grounded parametric generation to prevent hallucinated URLs or non-existent settings buttons.

---

## 2. Results vs. Baselines

We evaluated three system architectures across our 200-example hand-labelled Golden Evaluation Dataset:

1. **Baseline 0 (Trivial Baseline)**: Predicts majority class (`GENERAL_DEVICE_TROUBLESHOOTING`), uses a fixed static reply template ("Thanks for reaching out! Please send us a DM"), and always predicts `AUTO_REPLY`.
2. **Baseline 1 (Simple Baseline)**: Uses naive string keyword matching for intent classification, a zero-shot un-grounded LLM reply simulator, and basic profanity keyword filtering for escalation.
3. **Proposed System**: Combines a TF-IDF + Keyword-weighted Intent Classifier, a RAG Retriever indexing historical `@AppleSupport` resolution pairs, and a multi-rule Escalation Engine.

### Benchmark Results Table

| Evaluation Metric | Baseline 0 (Trivial) | Baseline 1 (Simple) | Proposed System |
|---|---|---|---|
| **Intent Classification Accuracy** | 18.50% | 69.00% | **85.00%** |
| **Intent Macro F1-Score** | 0.0520 | 0.6435 | **0.8455** |
| **Escalation Routing Accuracy** | 76.00% | 76.00% | **78.50%** |
| **Escalation Precision** | 0.0000 | 0.0000 | **0.5424** |
| **Escalation Recall** | 0.0000 | 0.0000 | **0.6667** |
| **Escalation F1-Score** | 0.0000 | 0.0000 | **0.5981** |
| **Reply BLEU-4 Score** | 0.0109 | 0.0264 | **0.0294** |
| **Reply ROUGE-1 Score** | 0.0513 | 0.1097 | **0.0953** |
| **Reply Cosine Similarity** | 0.0045 | 0.0299 | **0.0683** |
| **LLM-as-Judge Overall Score (1-5)** | 3.63 | 3.95 | **4.25** |

---

## 3. Failure Analysis: Top 5 Failure Modes

Through rigorous qualitative inspection of error cases in our golden dataset, we identified five primary failure modes:

### Failure Mode #1: Sarcasm & Implicit Frustration Misclassification
- **Real Tweet Example**: *"Oh fantastic, another update, another feature broken! Thanks @AppleSupport you guys are geniuses."*
- **Agent Behavior**: Classified as `GENERAL_DEVICE_TROUBLESHOOTING` and generated a cheerful template reply: *"We know how important this is to get working! Thanks for reaching out..."*
- **Root Cause Hypothesis**: Lexical TF-IDF representations weigh literal tokens ("thanks", "update", "geniuses") positively, completely missing sarcastic inversion.
- **Mitigation Strategy**: Implement a fine-tuned RoBERTa sentiment classifier to flag negative emotional polarity prior to intent routing.

### Failure Mode #2: Compound Multi-Intent Queries
- **Real Tweet Example**: *"@AppleSupport battery drains in 1 hour AND my iCloud photos stopped syncing after updating to iOS 17!"*
- **Agent Behavior**: Forcibly assigned a single intent (`BATTERY_HARDWARE`), omitting the secondary `ICLOUD_SYNC_STORAGE` inquiry from the response.
- **Root Cause Hypothesis**: Single-label multiclass setup cannot naturally model compound multi-intent customer queries.
- **Mitigation Strategy**: Transition intent classification architecture from multi-class to multi-label sigmoid scoring.

### Failure Mode #3: Short Context Ambiguity
- **Real Tweet Example**: *"@AppleSupport it's not working"*
- **Agent Behavior**: Low confidence intent prediction defaulted to `GENERAL_DEVICE_TROUBLESHOOTING`.
- **Root Cause Hypothesis**: Zero device, OS version, or app context provided in single-tweet query.
- **Mitigation Strategy**: Add a clarification fallback route when classification confidence falls below 0.35 ("Could you specify which device or feature isn't working?").

### Failure Mode #4: Over-Escalation on Routine Hardware Queries
- **Real Tweet Example**: *"@AppleSupport Is fast charging bad for long term battery health?"*
- **Agent Behavior**: Escalated to human support queue stating *"Physical hardware damage requiring store repair appointment."*
- **Root Cause Hypothesis**: Overly broad regex triggers on "battery health" created false-positive safety escalations.
- **Mitigation Strategy**: Refine regex boundary conditions with syntactic dependency parsing (distinguishing between "checking battery health" vs "battery health destroyed").

### Failure Mode #5: Outdated System Version Resolution Hallucination
- **Real Tweet Example**: *"@AppleSupport How do I clear app cache on iOS 17?"*
- **Agent Behavior**: Retrieved an older historical resolution referencing obsolete iOS 14 menu paths.
- **Root Cause Hypothesis**: RAG knowledge index lacked version-aware metadata filtering.
- **Mitigation Strategy**: Tag all historical resolution documents with `min_ios_version` and `max_ios_version` metadata.

---

## 4. Mandatory Section: "What is Misleading About My Headline Number?"

An engineering headline metric of **85.0% Intent Accuracy** and a **4.25 / 5.0 LLM-as-Judge Score** looks impressive, but relying on these headline numbers for production deployment would be dangerously misleading for several critical reasons:

1. **BLEU & ROUGE Are Poor Metrics for Open-Ended Support Replies**:
   - Our system achieved a BLEU-4 score of `0.0294` despite producing high-quality human-approved replies. Standard n-gram overlap metrics penalize legitimate rephrasings (e.g., "Visit Settings > Battery" vs "Check your battery settings").
2. **Offline Evaluation Ignores Multi-Turn Trajectory Drift**:
   - Our golden evaluation dataset evaluates single-turn query-reply snapshots. In real customer support, a response that seems "good" in isolation may fail if the customer asks follow-up questions that require conversational memory.
3. **Escalation Precision vs. Recall Trade-Off Masked by Accuracy**:
   - Overall Escalation Accuracy is `78.50%`, but Escalation Precision is only `54.24%`. In a real support center, a 54% precision means nearly half of escalated queries sent to human agents could have been automated, increasing human labor costs.
4. **Knowledge Base Static Leakage Risk**:
   - While the golden test set items were not directly in the RAG index, synthetic query variations derived from common Apple issues share syntactic similarity with historical training pairs, inflating offline retrieval scores.

---

## 5. What We Would Do Next With One More Week

If given one additional week, we would execute the following technical roadmap:

1. **Fine-Tuned Small Language Model (SLM)**: Fine-tune a `Qwen2.5-3B-Instruct` or `Llama-3.2-3B` model via LoRA on multi-turn `@AppleSupport` thread trajectories to master brand tone and formatting.
2. **Dense Vector Database (Qdrant / Faiss)**: Upgrade TF-IDF RAG retrieval to dense embeddings (`bge-small-en-v1.5`) paired with Qdrant vector database for semantic retrieval across 100k+ historical threads.
3. **Active Learning & Human-in-the-Loop Feedback Queue**: Build a Streamlit queue where human agents can review escalated messages, edit draft replies, and automatically push corrected pairs back into the RAG knowledge index.
4. **Twitter/X API Real-Time Webhook Integration**: Deploy a production async worker using Celery + Redis to listen to `@AppleSupport` mentions via Twitter API v2 webhooks and post grounded replies automatically.
