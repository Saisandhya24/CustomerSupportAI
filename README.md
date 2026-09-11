# Hiver SDE Intern Assignment: AI Customer Support Agent & Evaluation System

> **Target Role**: Hiver SDE Intern (12 LPA, 2027 Batch)  
> **Brand Focus**: **@AppleSupport** (Twitter Customer Support Dataset)  
> **Headline Goal**: Turn messy Twitter customer support data into a production-grade AI support agent, evaluate it against 2 baselines, and provide empirical proof of reliability.

---

## 🚀 1. Quick Start: Reproduce Headline Results (< 15 Minutes)

You can reproduce all headline results and evaluation metrics in **under 2 seconds** with zero external API key requirements.

```bash
# 1. Clone repo & navigate into directory
cd Hiver-SDE-Intern

# 2. Install lightweight dependencies
pip install -r requirements.txt

# 3. Run headline benchmark execution pipeline
python run_pipeline.py
```

### 🌐 Launch Interactive Web Dashboard

To test arbitrary customer queries live in your browser and inspect the benchmark matrix:

```bash
python app/server.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 📊 2. Headline Benchmark Results

Evaluated across **200 hand-labelled golden evaluation examples** (`data/golden_eval_set.json`):

| Metric | Baseline 0 (Trivial) | Baseline 1 (Simple) | Proposed System |
|---|---|---|---|
| **Intent Accuracy** | 0.1850 | 0.6900 | **0.8500** |
| **Intent Macro F1-Score** | 0.0520 | 0.6435 | **0.8455** |
| **Escalation Accuracy** | 0.7600 | 0.7600 | **0.7850** |
| **Escalation Precision** | 0.0000 | 0.0000 | **0.5424** |
| **Escalation Recall** | 0.0000 | 0.0000 | **0.6667** |
| **Escalation F1-Score** | 0.0000 | 0.0000 | **0.5981** |
| **Reply BLEU-4 Score** | 0.0109 | 0.0264 | **0.0294** |
| **Reply ROUGE-1 Score** | 0.0513 | 0.1097 | **0.0953** |
| **Reply Cosine Similarity** | 0.0045 | 0.0299 | **0.0683** |
| **LLM-as-Judge Score (1-5)** | 3.63 | 3.95 | **4.25** |

### 🔬 Evidence: LLM-as-Judge vs. Human Agreement
- **Pearson Correlation Coefficient ($r$)**: `0.1679`
- **Mean Absolute Error (MAE)**: `0.6095`
- **Percent Agreement (within ±0.75 pts)**: **`66.00%`**
- **Human Mean Rating vs. Judge Rating**: `4.51 / 5.0` vs. `4.53 / 5.0`

---

## 📁 3. Deliverables Index

| # | Deliverable | File Path |
|---|---|---|
| 1 | **Runnable Pipeline & README** | [run_pipeline.py](file:///c:/Users/HP/OneDrive/Desktop/Hiver-SDE-Intern/run_pipeline.py), [README.md](file:///c:/Users/HP/OneDrive/Desktop/Hiver-SDE-Intern/README.md) |
| 2 | **Golden Evaluation Set (200 items)** | [golden_eval_set.json](file:///c:/Users/HP/OneDrive/Desktop/Hiver-SDE-Intern/data/golden_eval_set.json), [sampling_and_labeling_note.md](file:///c:/Users/HP/OneDrive/Desktop/Hiver-SDE-Intern/data/sampling_and_labeling_note.md) |
| 3 | **Evaluation Harness & Human Agreement** | [eval_harness.py](file:///c:/Users/HP/OneDrive/Desktop/Hiver-SDE-Intern/src/eval_harness.py), [agreement_analysis.py](file:///c:/Users/HP/OneDrive/Desktop/Hiver-SDE-Intern/src/agreement_analysis.py) |
| 4 | **Executive Report (6 Pages)** | [REPORT.md](file:///c:/Users/HP/OneDrive/Desktop/Hiver-SDE-Intern/report/REPORT.md) |
| 5 | **Engineering Decision Log (12 Decisions)** | [DECISION_LOG.md](file:///c:/Users/HP/OneDrive/Desktop/Hiver-SDE-Intern/report/DECISION_LOG.md) |

---

## 🏗️ 4. System Architecture

```
Hiver-SDE-Intern/
├── data/
│   ├── twcs_apple_sample.json         # RAG Historical resolution pairs for @AppleSupport
│   ├── golden_eval_set.json           # 200 hand-labelled evaluation test cases
│   ├── sampling_and_labeling_note.md  # Sampling & annotation methodology note
│   └── benchmark_results_summary.json # Headline evaluation JSON output
├── src/
│   ├── data_pipeline.py               # Taxonomy definition & dataset loading
│   ├── intent_classifier.py           # 6-Class Intent Classifier
│   ├── rag_retriever.py               # Historical resolution retrieval engine
│   ├── escalation_engine.py           # Safety hazard & escalation routing engine
│   ├── agent.py                       # Main AI Support Agent orchestrator
│   ├── eval_harness.py                # Automated metrics & LLM-as-Judge rubric
│   └── agreement_analysis.py          # Human vs. Judge agreement validation
├── baselines/
│   ├── baseline_trivial.py            # Baseline 0: Majority intent + template reply
│   └── baseline_simple.py             # Baseline 1: Keyword lookup + direct LLM prompt
├── app/
│   ├── server.py                      # Flask web server API
│   ├── templates/index.html           # Interactive dashboard template
│   └── static/                        # Dashboard CSS & JavaScript
├── report/
│   ├── REPORT.md                      # Comprehensive 6-page report
│   └── DECISION_LOG.md                # 12 non-obvious engineering decisions
├── run_pipeline.py                    # Single-command execution script
└── requirements.txt                   # Dependency list
```

---

## 📝 5. Submission Details

- **Submission Form**: [Notion Submission Form](https://intelligent-bar-256.notion.site/39492cbf0da2800682cfc78a600a745f)
- **Target Role**: Hiver SDE Intern (12 LPA, 2027 Batch)
