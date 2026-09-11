"""
RAG Retriever Engine
Indexes historical Twitter Customer Support resolution pairs and retrieves grounded context.
"""

from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class RAGRetriever:
    def __init__(self, knowledge_base: List[Dict[str, Any]]):
        self.kb = knowledge_base
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        
        # Build index from customer queries & resolutions
        self.documents = [
            f"{item['customer_query']} {item['brand_resolution']} {item['resolution_category']}"
            for item in self.kb
        ]
        self.index_vectors = self.vectorizer.fit_transform(self.documents)

    def retrieve(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """
        Retrieves top_k historical resolution items matching the query.
        """
        clean_q = self._clean_text(query)
        q_vec = self.vectorizer.transform([clean_q])
        sims = cosine_similarity(q_vec, self.index_vectors)[0]
        
        # Sort indices by similarity descending
        top_indices = sims.argsort()[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            similarity_score = float(sims[idx])
            item = self.kb[idx].copy()
            item["similarity_score"] = round(similarity_score, 4)
            results.append(item)
            
        return results

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        return text.lower().strip()
