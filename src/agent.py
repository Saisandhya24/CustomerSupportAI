"""
AI Support Agent Orchestrator
Combines Intent Classifier, RAG Retriever, and Escalation Engine to process customer messages,
make routing decisions, and draft grounded brand responses.
"""

from typing import Dict, Any, List
from src.intent_classifier import IntentClassifier
from src.rag_retriever import RAGRetriever
from src.escalation_engine import EscalationEngine
from src.data_pipeline import DataPipeline

class SupportAgent:
    def __init__(self, data_dir: str = "data"):
        self.pipeline = DataPipeline(data_dir=data_dir)
        self.kb = self.pipeline.load_knowledge_base()
        
        self.classifier = IntentClassifier()
        self.retriever = RAGRetriever(knowledge_base=self.kb)
        self.escalation_engine = EscalationEngine()

    def process_message(self, tweet_text: str) -> Dict[str, Any]:
        """
        Main end-to-end pipeline execution for an incoming customer tweet.
        """
        # 1. Intent Classification
        intent, confidence, all_intent_scores = self.classifier.classify(tweet_text)
        
        # 2. RAG Historical Context Retrieval
        retrieved_contexts = self.retriever.retrieve(tweet_text, top_k=2)
        
        # 3. Escalation Decision
        action, escalation_reason = self.escalation_engine.evaluate(
            query=tweet_text,
            intent=intent,
            confidence=confidence
        )
        
        # 4. Draft Grounded Response
        draft_reply = self._draft_reply(
            tweet_text=tweet_text,
            intent=intent,
            action=action,
            escalation_reason=escalation_reason,
            rag_contexts=retrieved_contexts
        )
        
        return {
            "tweet_text": tweet_text,
            "predicted_intent": intent,
            "intent_confidence": confidence,
            "action": action,
            "escalation_reason": escalation_reason,
            "retrieved_context": retrieved_contexts,
            "draft_reply": draft_reply
        }

    def _draft_reply(self, tweet_text: str, intent: str, action: str, escalation_reason: str, rag_contexts: List[Dict[str, Any]]) -> str:
        """
        Synthesizes a grounded reply matching AppleSupport brand voice using RAG context.
        """
        best_resolution = rag_contexts[0]["brand_resolution"] if rag_contexts else ""
        
        if action == "ESCALATE":
            return f"We're here to help! Because your issue requires specialized account or hardware assistance ({escalation_reason}), please send us a Direct Message so an advisor can assist: twitter.com/messages/compose?recipient_id=AppleSupport"
        
        # Safe AUTO_REPLY grounded synthesis
        if best_resolution:
            # Cleanly adapt retrieved historical resolution
            return f"We know how important this is to get working! {best_resolution}"
        else:
            return "We'd love to help you get this resolved! Please check your settings or restart your device. If the issue continues, reach out to us via DM."
