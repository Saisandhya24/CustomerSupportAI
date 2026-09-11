"""
Baseline 1: Simple Baseline
- Naive keyword-matching intent classification
- Direct zero-shot LLM reply draft (no RAG historical context)
- Keyword profanity escalation filter
"""

from typing import Dict, Any
import re

class BaselineSimple:
    def __init__(self):
        self.keywords = {
            "BATTERY_HARDWARE": ["battery", "charge", "screen", "repair"],
            "IOS_UPDATE_SOFTWARE": ["ios", "update", "freeze", "crash", "lag"],
            "APPLE_ID_ACCOUNT": ["apple id", "password", "locked", "account"],
            "ICLOUD_SYNC_STORAGE": ["icloud", "storage", "sync", "backup"],
            "APP_STORE_PURCHASE": ["app store", "refund", "billed", "subscription"],
            "GENERAL_DEVICE_TROUBLESHOOTING": ["wifi", "bluetooth", "airpods", "speaker"]
        }

    def process_message(self, tweet_text: str) -> Dict[str, Any]:
        text_lower = tweet_text.lower()
        
        # 1. Naive Intent Keyword Classifier
        best_intent = "GENERAL_DEVICE_TROUBLESHOOTING"
        max_matches = 0
        for intent, kw_list in self.keywords.items():
            matches = sum(1 for kw in kw_list if kw in text_lower)
            if matches > max_matches:
                max_matches = matches
                best_intent = intent
                
        # 2. Profanity / Crude Escalation Filter
        if any(w in text_lower for w in ["fuck", "shit", "damn", "scam"]):
            action = "ESCALATE"
            reason = "Profanity detected in customer tweet."
        else:
            action = "AUTO_REPLY"
            reason = "Keyword check passed."
            
        # 3. Direct ungrounded zero-shot reply (No RAG)
        draft_reply = f"We hear your concern regarding {best_intent.lower().replace('_', ' ')}. Please make sure your iPhone is updated to the latest software and try restarting it."

        return {
            "tweet_text": tweet_text,
            "predicted_intent": best_intent,
            "intent_confidence": 0.6 if max_matches > 0 else 0.3,
            "action": action,
            "escalation_reason": reason,
            "draft_reply": draft_reply
        }
