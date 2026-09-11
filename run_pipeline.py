"""
Main Pipeline Runner for Hiver SDE Intern Assignment
Executes baseline 0 (trivial), baseline 1 (simple), and proposed AI Support Agent
against the 200-example golden evaluation set. Outputs clean benchmark metrics table
and human-vs-judge agreement proof in under 15 minutes.
"""

import time
import json
import sys
import io

# Force UTF-8 output encoding for Windows compatibility
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.data_pipeline import DataPipeline
from src.agent import SupportAgent
from baselines.baseline_trivial import BaselineTrivial
from baselines.baseline_simple import BaselineSimple
from src.eval_harness import EvaluationHarness
from src.agreement_analysis import AgreementAnalyzer

def main():
    start_time = time.time()
    print("=" * 80)
    print(" HIVER SDE INTERN ASSIGNMENT: AI CUSTOMER SUPPORT AGENT PIPELINE ")
    print(" Target Brand: @AppleSupport (Twitter Customer Support Dataset)")
    print("=" * 80)
    
    # 1. Initialize Pipeline & Load Golden Dataset
    data_pipe = DataPipeline()
    golden_set = data_pipe.load_golden_set()
    print(f"Loaded Golden Evaluation Dataset: {len(golden_set)} items.")

    harness = EvaluationHarness()
    analyzer = AgreementAnalyzer()

    # 2. Evaluate Baseline 0 (Trivial)
    print("\n[1/3] Running Baseline 0 (Trivial Majority Baseline)...")
    b0 = BaselineTrivial()
    res_b0 = harness.evaluate_dataset(b0, golden_set)

    # 3. Evaluate Baseline 1 (Simple)
    print("[2/3] Running Baseline 1 (Simple Keyword + Direct Zero-Shot LLM)...")
    b1 = BaselineSimple()
    res_b1 = harness.evaluate_dataset(b1, golden_set)

    # 4. Evaluate Proposed System (Intent + RAG + Escalation Router)
    print("[3/3] Running Proposed System (Intent Classifier + RAG + Escalation Engine)...")
    agent = SupportAgent()
    res_proposed = harness.evaluate_dataset(agent, golden_set)

    # 5. Evaluate Judge vs Human Agreement
    agreement_metrics = analyzer.compute_agreement(res_proposed["predictions"])

    elapsed_time = round(time.time() - start_time, 2)

    # 6. Format Headline Results Comparison Table
    print("\n" + "=" * 97)
    print(f" HEADLINE EVALUATION RESULTS BENCHMARK (Completed in {elapsed_time}s)")
    print("=" * 97)
    print(f"{'Metric':<32} | {'Baseline 0 (Trivial)':<20} | {'Baseline 1 (Simple)':<20} | {'Proposed System':<20}")
    print("-" * 97)
    print(f"{'Intent Accuracy':<32} | {res_b0['intent_accuracy']:<20.4f} | {res_b1['intent_accuracy']:<20.4f} | {res_proposed['intent_accuracy']:<20.4f}")
    print(f"{'Intent Macro F1':<32} | {res_b0['intent_macro_f1']:<20.4f} | {res_b1['intent_macro_f1']:<20.4f} | {res_proposed['intent_macro_f1']:<20.4f}")
    print(f"{'Escalation Accuracy':<32} | {res_b0['escalation_accuracy']:<20.4f} | {res_b1['escalation_accuracy']:<20.4f} | {res_proposed['escalation_accuracy']:<20.4f}")
    print(f"{'Escalation Precision':<32} | {res_b0['escalation_precision']:<20.4f} | {res_b1['escalation_precision']:<20.4f} | {res_proposed['escalation_precision']:<20.4f}")
    print(f"{'Escalation Recall':<32} | {res_b0['escalation_recall']:<20.4f} | {res_b1['escalation_recall']:<20.4f} | {res_proposed['escalation_recall']:<20.4f}")
    print(f"{'Escalation F1':<32} | {res_b0['escalation_f1']:<20.4f} | {res_b1['escalation_f1']:<20.4f} | {res_proposed['escalation_f1']:<20.4f}")
    print(f"{'Reply BLEU-4':<32} | {res_b0['bleu_4']:<20.4f} | {res_b1['bleu_4']:<20.4f} | {res_proposed['bleu_4']:<20.4f}")
    print(f"{'Reply ROUGE-1':<32} | {res_b0['rouge_1']:<20.4f} | {res_b1['rouge_1']:<20.4f} | {res_proposed['rouge_1']:<20.4f}")
    print(f"{'Reply Cosine Similarity':<32} | {res_b0['cosine_similarity']:<20.4f} | {res_b1['cosine_similarity']:<20.4f} | {res_proposed['cosine_similarity']:<20.4f}")
    print(f"{'LLM-as-Judge Score (1-5)':<32} | {res_b0['judge_overall_score']:<20.2f} | {res_b1['judge_overall_score']:<20.2f} | {res_proposed['judge_overall_score']:<20.2f}")
    print("=" * 97)

    # 7. Print Judge vs Human Agreement Metrics
    print("\n" + "=" * 70)
    print(" EVIDENCE: LLM-AS-JUDGE VS. HUMAN AGREEMENT METRICS ")
    print("=" * 70)
    print(f" Pearson Correlation Coefficient (r) : {agreement_metrics['pearson_correlation']:.4f}")
    print(f" Cohen's Kappa (kappa)              : {agreement_metrics['cohens_kappa']:.4f}")
    print(f" Mean Absolute Error (MAE)           : {agreement_metrics['mean_absolute_error']:.4f}")
    print(f" Percent Agreement (within 0.75 pts) : {agreement_metrics['percent_agreement']:.2f}%")
    print(f" Human Mean Rating vs. Judge Rating  : {agreement_metrics['human_mean_score']} / 5.0 vs. {agreement_metrics['judge_mean_score']} / 5.0")
    print("=" * 70)

    # Save summary results JSON
    summary_output = {
        "execution_time_seconds": elapsed_time,
        "baseline_0_trivial": res_b0,
        "baseline_1_simple": res_b1,
        "proposed_system": res_proposed,
        "human_judge_agreement": agreement_metrics
    }
    
    with open("data/benchmark_results_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_output, f, indent=2)

    print("\nResults successfully saved to data/benchmark_results_summary.json")

if __name__ == "__main__":
    main()
