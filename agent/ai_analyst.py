# agent/ai_analyst.py

def generate_ai_answer(query_type, metrics):

    total_deals = metrics.get("total_deals", 0)
    total_value = metrics.get("total_pipeline_value", 0)

    sector_counts = metrics.get("deals_by_sector")
    stage_counts = metrics.get("deals_by_stage")

    if sector_counts is not None and not sector_counts.empty:
        top_sector = sector_counts.idxmax()
        top_sector_value = sector_counts.max()
    else:
        top_sector = "Unknown"
        top_sector_value = 0

    if stage_counts is not None and not stage_counts.empty:
        top_stage = stage_counts.idxmax()
        top_stage_value = stage_counts.max()
    else:
        top_stage = "Unknown"
        top_stage_value = 0


    if query_type == "pipeline_summary":

        return f"""
Pipeline overview:

• Total deals: **{total_deals}**
• Total pipeline value: **₹{total_value:,.0f}**
• Strongest sector: **{top_sector}**
• Most active stage: **{top_stage}**
"""


    if query_type == "risky_deals":

        return """
Deals listed below have risk indicators such as overdue close dates, missing deal information, or stalled progress.

These opportunities may require immediate sales attention.
"""


    if query_type == "pipeline_bottleneck":

        return """
Many deals appear concentrated in one stage of the pipeline.

This suggests a potential bottleneck where deals are not progressing efficiently.
"""


    if query_type == "sector_analysis":

        return f"""
The **{top_sector}** sector currently contains the highest number of opportunities with **{top_sector_value} deals**.

This sector represents the strongest current demand.
"""


    if query_type == "top_deals":

        return """
The deals listed below represent the highest-value opportunities in the pipeline.
"""


    if query_type == "closing_soon":

        return """
The deals below are expected to close within the next 30 days.
"""


    if query_type == "revenue_forecast":

        return """
The forecast below estimates expected revenue from the pipeline based on deal stage probabilities.
"""


    if query_type == "anomaly_detection":

        return """
The system analyzed the dataset for missing or inconsistent deal information.
"""


    return "I analyzed the pipeline data and generated the relevant results below."