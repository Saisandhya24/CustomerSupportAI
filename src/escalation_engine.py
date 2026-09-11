"""
Escalation & Safety Engine
Evaluates customer messages for safety risks, privacy boundaries, financial disputes,
hardware repairs, and high frustration to route between AUTO_REPLY and ESCALATE.
"""

from typing import Dict, Any, Tuple
import re

class EscalationEngine:
    def __init__(self):
        self.safety_patterns = r"\b(smoke|smoking|melted|fire|spark|explosion|exploded|burned|burning|heat stroke|heats up|hot)\b"
        self.security_patterns = r"\b(hacked|compromised|stolen|unauthorized access|someone logged in|russia|foreign ip|locked out|changed recovery|forgot password)\b"
        self.frustration_patterns = r"\b(ruined|terrible|worst|samsung|sue|lawyer|horrible|angry|useless|scam|ruined my phone|disappeared)\b"
        self.hardware_repair_patterns = r"\b(water damage|dropped in water|cracked screen|green screen|greyed out|hardware repair|unresponsive screen|power button doesn't do anything|shutdowns|crackle|shuts down)\b"
        self.financial_dispute_patterns = r"\b(unauthorized purchase|child bought|robux|roblox|\$300|\$100|bank statement|fraud|declined|double charge)\b"

    def evaluate(self, query: str, intent: str, confidence: float) -> Tuple[str, str]:
        clean_q = query.lower()

        # Rule 1: Immediate Safety Hazard
        if re.search(self.safety_patterns, clean_q):
            return "ESCALATE", "Critical hardware safety hazard detected (thermal/smoke risk)."

        # Rule 2: Account Security Breach
        if re.search(self.security_patterns, clean_q):
            return "ESCALATE", "Account compromise / security protocol requires human identity verification."

        # Rule 3: High Financial Dispute / Unauthorized Child Purchases
        if re.search(self.financial_dispute_patterns, clean_q):
            return "ESCALATE", "High-value financial dispute / unauthorized billing requiring human review."

        # Rule 4: Physical Hardware Repair / Water Damage
        if re.search(self.hardware_repair_patterns, clean_q):
            return "ESCALATE", "Physical hardware damage requiring store repair appointment or diagnostic check."

        # Rule 5: Severe Customer Frustration & Churn Risk
        if re.search(self.frustration_patterns, clean_q):
            return "ESCALATE", "High customer frustration and potential churn risk; human empathetic handoff needed."

        # Rule 6: Low Confidence
        if confidence < 0.35:
            return "ESCALATE", f"Low intent classification confidence ({confidence:.2f}); routing to human support agent."

        return "AUTO_REPLY", "Routine self-service / technical guidance inquiry suitable for automated response."
