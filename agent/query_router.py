# agent/query_router.py

"""
Query Router

Routes detected intent to the correct analytics function.
"""

from analytics.pipeline_metrics import (
    pipeline_summary,
    pipeline_value_by_sector,
    pipeline_bottlenecks,
    deals_closing_soon,
    top_deals,
    detect_anomalies
)

from analytics.deal_health import get_risky_deals
from analytics.pipeline_forecast import pipeline_forecast


def route_query(intent, df):

    if intent == "pipeline_summary":
        return pipeline_summary(df)

    elif intent == "sector_analysis":
        return pipeline_value_by_sector(df)

    elif intent == "stage_analysis":
        return pipeline_summary(df)

    elif intent == "closing_soon":
        return deals_closing_soon(df)

    elif intent == "top_deals":
        return top_deals(df)

    elif intent == "risky_deals":
        return get_risky_deals(df)

    elif intent == "pipeline_bottleneck":
        return pipeline_bottlenecks(df)

    elif intent == "anomaly_detection":
        return detect_anomalies(df)

    elif intent == "revenue_forecast":
        return pipeline_forecast(df)

    return None