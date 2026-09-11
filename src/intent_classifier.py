"""
Intent Classifier Engine
Classifies customer tweets into the 6 Apple Support intent categories.
"""

from typing import Dict, Any, Tuple
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.data_pipeline import INTENT_TAXONOMY

class IntentClassifier:
    def __init__(self):
        self.taxonomy = INTENT_TAXONOMY
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        
        self.intent_labels = list(self.taxonomy.keys())
        self.intent_docs = []
        for label in self.intent_labels:
            doc = self.taxonomy[label]["description"] + " " + " ".join(self.taxonomy[label]["keywords"] * 5)
            self.intent_docs.append(doc)
            
        self.doc_vectors = self.vectorizer.fit_transform(self.intent_docs)

    def classify(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        clean_text = self._clean_text(text)
        query_vec = self.vectorizer.transform([clean_text])
        similarities = cosine_similarity(query_vec, self.doc_vectors)[0]
        
        keyword_scores = {}
        for idx, label in enumerate(self.intent_labels):
            kw_match = 0
            keywords = self.taxonomy[label]["keywords"]
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', clean_text, re.IGNORECASE):
                    kw_match += 1
            kw_boost = min(0.5, kw_match * 0.20)
            combined_score = float(similarities[idx]) * 0.5 + kw_boost
            keyword_scores[label] = round(combined_score, 4)

        best_label = max(keyword_scores, key=keyword_scores.get)
        confidence = keyword_scores[best_label]
        norm_confidence = min(1.0, confidence * 1.8)
        
        return best_label, round(norm_confidence, 4), keyword_scores

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        return text.lower().strip()
