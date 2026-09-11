"""
Baseline 0: Trivial Baseline
- Predicts majority intent (GENERAL_DEVICE_TROUBLESHOOTING)
- Fixed static reply template
- Fixed AUTO_REPLY route
"""

from typing import Dict, Any

class BaselineTrivial:
    def process_message(self, tweet_text: str) -> Dict[str, Any]:
        return {
            "tweet_text": tweet_text,
            "predicted_intent": "GENERAL_DEVICE_TROUBLESHOOTING",
            "intent_confidence": 0.5,
            "action": "AUTO_REPLY",
            "escalation_reason": "Default trivial baseline route.",
            "draft_reply": "Thanks for reaching out to us! Please send us a DM so we can look into this for you."
        }
