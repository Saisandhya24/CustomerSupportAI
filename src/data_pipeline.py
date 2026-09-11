"""
Data Pipeline for Twitter Customer Support Dataset (@AppleSupport)
Handles loading, taxonomy definition, thread pair parsing, and golden evaluation dataset loading.
"""

import json
import os
from typing import List, Dict, Any

# Define Apple Support Intent Taxonomy
INTENT_TAXONOMY = {
    "BATTERY_HARDWARE": {
        "description": "Issues related to battery health, rapid drain, overheating, charging port, or physical hardware repairs.",
        "keywords": ["battery", "drain", "charge", "charging", "overheat", "hot", "screen repair", "battery health", "power off"]
    },
    "IOS_UPDATE_SOFTWARE": {
        "description": "Issues resulting from iOS updates, software bugs, app crashes, frozen screen, or system bootloops.",
        "keywords": ["ios", "update", "ios 17", "ios 16", "update failed", "freeze", "froze", "lag", "bug", "crash", "restart loop"]
    },
    "APPLE_ID_ACCOUNT": {
        "description": "Issues regarding Apple ID login, locked accounts, password reset, 2FA codes, or security verification.",
        "keywords": ["apple id", "password", "locked", "two-factor", "2fa", "verification code", "sign in", "security questions", "disabled"]
    },
    "ICLOUD_SYNC_STORAGE": {
        "description": "Problems with iCloud storage capacity, photo syncing, backup restoration, or Drive file access.",
        "keywords": ["icloud", "storage", "sync", "backup", "photos sync", "icloud drive", "storage full", "restore backup"]
    },
    "APP_STORE_PURCHASE": {
        "description": "Inquiries about App Store billing, double charges, accidental subscription renewals, or refund requests.",
        "keywords": ["app store", "purchase", "refund", "subscription", "billed", "charged", "payment method", "in-app purchase"]
    },
    "GENERAL_DEVICE_TROUBLESHOOTING": {
        "description": "General connectivity issues (Wi-Fi, Bluetooth, Cellular), sound/speaker problems, camera glitches, or general usage support.",
        "keywords": ["wifi", "wi-fi", "bluetooth", "cellular", "no service", "speaker", "microphone", "camera", "airpods", "airdrop"]
    }
}

class DataPipeline:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.kb_path = os.path.join(data_dir, "twcs_apple_sample.json")
        self.golden_path = os.path.join(data_dir, "golden_eval_set.json")

    def load_knowledge_base(self) -> List[Dict[str, Any]]:
        """Loads historical resolution threads used for RAG grounding."""
        if not os.path.exists(self.kb_path):
            raise FileNotFoundError(f"Knowledge base file not found at {self.kb_path}")
        with open(self.kb_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_golden_set(self) -> List[Dict[str, Any]]:
        """Loads the 200-example hand-labelled golden evaluation dataset."""
        if not os.path.exists(self.golden_path):
            raise FileNotFoundError(f"Golden dataset file not found at {self.golden_path}")
        with open(self.golden_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_taxonomy_summary(self) -> Dict[str, str]:
        """Returns intent taxonomy descriptions."""
        return {k: v["description"] for k, v in INTENT_TAXONOMY.items()}
