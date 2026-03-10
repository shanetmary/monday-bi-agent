# agent/query_parser.py

"""
Query Parser

Detects user intent from a natural language question.
First tries the LLM (TinyLlama via Ollama),
then falls back to keyword matching.
"""

from agent.llm_intent import detect_intent_llm


INTENT_KEYWORDS = {

    "pipeline_summary": [
        "pipeline",
        "overall",
        "summary",
        "status",
        "performance",
        "how is our pipeline"
    ],

    "sector_analysis": [
        "sector",
        "industry",
        "which sector",
        "sector performance"
    ],

    "stage_analysis": [
        "stage",
        "funnel",
        "progress",
        "pipeline stage"
    ],

    "closing_soon": [
        "close",
        "closing",
        "closing soon",
        "next 30 days",
        "upcoming"
    ],

    "top_deals": [
        "biggest",
        "largest",
        "top deals",
        "highest value",
        "largest deals"
    ],

    "risky_deals": [
        "risky",
        "risk",
        "at risk",
        "problem deals"
    ],

    "pipeline_bottleneck": [
        "stuck",
        "bottleneck",
        "where is pipeline stuck"
    ],

    "anomaly_detection": [
        "missing",
        "data issue",
        "anomaly",
        "data problem"
    ],

    "revenue_forecast": [
        "forecast",
        "expected revenue",
        "revenue prediction",
        "revenue forecast"
    ]
}


def parse_query(question: str) -> str:
    """
    Detect intent from user question.
    """

    # -------------------------------------------------
    # Step 1: Try LLM intent detection
    # -------------------------------------------------

    try:
        intent = detect_intent_llm(question)

        if intent in INTENT_KEYWORDS:
            return intent

    except Exception:
        pass


    # -------------------------------------------------
    # Step 2: Fallback keyword matching
    # -------------------------------------------------

    q = question.lower()

    for intent, keywords in INTENT_KEYWORDS.items():

        if any(keyword in q for keyword in keywords):
            return intent


    # -------------------------------------------------
    # Default
    # -------------------------------------------------

    return "pipeline_summary"