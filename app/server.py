"""
Flask Web Server for AI Support Agent Dashboard
Provides interactive APIs for real-time customer query testing and evaluation visualization.
"""

from flask import Flask, render_template, request, jsonify
import os
import json
from src.agent import SupportAgent

app = Flask(__name__, template_folder="templates", static_folder="static")

# Initialize Agent
agent = SupportAgent()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/process", methods=["POST"])
def process_query():
    data = request.get_json() or {}
    text = data.get("query", "").strip()
    if not text:
        return jsonify({"error": "Query cannot be empty"}), 400
    
    result = agent.process_message(text)
    return jsonify(result)

@app.route("/api/benchmark", methods=["GET"])
def get_benchmark():
    benchmark_path = os.path.join("data", "benchmark_results_summary.json")
    if os.path.exists(benchmark_path):
        with open(benchmark_path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Benchmark data not found. Please run run_pipeline.py first."}), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
