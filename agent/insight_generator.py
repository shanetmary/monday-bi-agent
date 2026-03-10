# agent/insight_generator.py

def generate_pipeline_insight(metrics, query_type):

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
### Pipeline Analysis

Your sales pipeline currently contains **{total_deals} active deals** with a combined potential value of **₹{total_value:,.0f}**.

The sector contributing the most opportunities is **{top_sector}**, which currently has **{top_sector_value} deals**.

From a pipeline progression perspective, the stage with the largest number of deals is **{top_stage}**, containing **{top_stage_value} opportunities**.

If a large number of deals remain in the same stage for extended periods, it may indicate a bottleneck in the sales process.
Monitoring stage movement can help improve deal conversion.
"""

    elif query_type == "sector_analysis":

        return f"""
### Sector Performance Insight

The **{top_sector} sector** currently dominates the pipeline with **{top_sector_value} deals**.

This suggests that most of the company's opportunities are concentrated in this industry segment.

If this trend continues, it may represent a strategic growth area for the company. However, diversification across sectors can help reduce business risk.
"""

    elif query_type == "stage_analysis":

        return f"""
### Sales Funnel Insight

The stage containing the highest number of deals is **{top_stage}**, with **{top_stage_value} deals currently in this phase.

If many opportunities remain in this stage for extended periods, it may indicate a slowdown in deal progression.

Tracking how deals move from this stage to the next can help improve pipeline efficiency and revenue conversion.
"""

    elif query_type == "closing_soon":

        return """
### Upcoming Closures

The deals displayed above are expected to close within the next **30 days** based on their tentative close dates.

These opportunities represent **near-term revenue potential** for the company.

Sales teams should prioritize engagement with these deals to maximize the likelihood of successful closure.
"""

    elif query_type == "top_deals":

        return """
### High Value Deal Insight

The deals listed above represent the **largest revenue opportunities** currently present in the pipeline.

Winning or losing a small number of these deals can significantly impact total revenue.

Leadership teams typically monitor high-value opportunities closely to ensure adequate attention and resources are allocated.
"""

    return "No additional insight available."