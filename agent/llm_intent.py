import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

import ollama

INTENTS = [
    "pipeline_summary",
    "sector_analysis",
    "stage_analysis",
    "closing_soon",
    "top_deals",
    "risky_deals",
    "pipeline_bottleneck",
    "anomaly_detection",
    "revenue_forecast"
]


def detect_intent_llm(question):

    prompt = f"""
You are an AI system that classifies business questions.

Your job is ONLY to return the correct intent.

Allowed intents:
{INTENTS}

Rules:
- Return ONLY the intent name
- No explanation
- No extra text

Question: {question}
"""

    response = ollama.chat(
        model="tinyllama",
        messages=[{"role": "user", "content": prompt}]
    )

    intent = response["message"]["content"].strip().lower()

    if intent in INTENTS:
        return intent

    return "pipeline_summary"