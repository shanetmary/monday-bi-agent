import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import matplotlib.pyplot as plt

from monday.fetch_boards import fetch_deals_board
from data_preprocessing.dataframe_builder import build_deals_dataframe

from analytics.pipeline_metrics import pipeline_summary
from analytics.pipeline_metrics import pipeline_value_by_sector
from analytics.pipeline_metrics import pipeline_funnel_chart

from agent.query_parser import parse_query
from agent.query_router import route_query
from agent.ai_analyst import generate_ai_answer


# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="AI BI Copilot",
    layout="wide"
)

st.title("AI Business Intelligence Copilot for Monday.com")

st.info(
    "Ask questions about your company's pipeline data from Monday.com. "
    "I can analyze deals, detect risks, and forecast revenue."
)


# -------------------------------------------------
# Cached Data Loading
# -------------------------------------------------

@st.cache_data
def load_data():
    data = fetch_deals_board()
    df = build_deals_dataframe(data)
    return df


df = load_data()

metrics = pipeline_summary(df)


# -------------------------------------------------
# KPI METRICS (Executive Cards)
# -------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Total Deals", metrics["total_deals"])

col2.metric(
    "Pipeline Value",
    f"₹{metrics['total_pipeline_value']:,.0f}"
)

col3.metric(
    "Active Sectors",
    df["sector"].nunique()
)


# -------------------------------------------------
# Executive Summary Button
# -------------------------------------------------

if st.button("Generate Executive Summary"):

    st.subheader("Executive Pipeline Overview")

    st.write(
        f"Total Deals: **{metrics['total_deals']}**"
    )

    st.write(
        f"Total Pipeline Value: **₹{metrics['total_pipeline_value']:,.0f}**"
    )

    top_sector = metrics["deals_by_sector"].idxmax()

    st.write(f"Strongest Sector: **{top_sector}**")

    st.subheader("Deals by Stage")

    st.bar_chart(metrics["deals_by_stage"])

    st.subheader("Pipeline Funnel")

    fig = pipeline_funnel_chart(df)

    st.pyplot(fig)


# -------------------------------------------------
# Chat Memory
# -------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------------------------------
# Suggested Questions
# -------------------------------------------------

if len(st.session_state.messages) == 0:

    st.markdown("### Try asking:")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("How is our pipeline looking?"):
            st.session_state.suggested_question = "How is our pipeline looking?"

        if st.button("Which deals are risky?"):
            st.session_state.suggested_question = "Which deals are risky?"

        if st.button("Where is our pipeline stuck?"):
            st.session_state.suggested_question = "Where is our pipeline stuck?"

    with col2:

        if st.button("Which sector has the strongest deals?"):
            st.session_state.suggested_question = "Which sector has the strongest deals?"

        if st.button("Show the biggest deals"):
            st.session_state.suggested_question = "Show the biggest deals"

        if st.button("What revenue might close from the pipeline?"):
            st.session_state.suggested_question = "What revenue might close from the pipeline?"


# -------------------------------------------------
# Display Chat History
# -------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# -------------------------------------------------
# Chat Input
# -------------------------------------------------

question = st.chat_input("Ask a business question")


if "suggested_question" in st.session_state:
    question = st.session_state.suggested_question
    del st.session_state["suggested_question"]


# -------------------------------------------------
# Chat Processing
# -------------------------------------------------

if question:

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing company pipeline data..."):

            query_type = parse_query(question)

            result = route_query(query_type, df)

            answer = generate_ai_answer(query_type, metrics)

            st.subheader("AI Insight")

            st.write(answer)


        # -------------------------------------------------
        # Data Quality
        # -------------------------------------------------

        if query_type == "anomaly_detection":

            st.subheader("Data Quality Report")

            if result:
                for issue in result:
                    st.write("•", issue)
            else:
                st.write("No major data issues detected.")


        # -------------------------------------------------
        # Risky Deals
        # -------------------------------------------------

        elif query_type == "risky_deals":

            st.subheader("Risky Deals")

            st.dataframe(result)


        # -------------------------------------------------
        # Pipeline Bottleneck
        # -------------------------------------------------

        elif query_type == "pipeline_bottleneck":

            st.subheader("Pipeline Bottleneck")

            stage, count = result

            st.write(
                f"Most deals are stuck in **{stage}** with **{count} deals**."
            )

            st.bar_chart(metrics["deals_by_stage"])


        # -------------------------------------------------
        # Top Deals
        # -------------------------------------------------

        elif query_type == "top_deals":

            st.subheader("Top Deals")

            st.dataframe(result)

            chart = result.set_index("deal_name")["deal_value"]

            st.bar_chart(chart)


        # -------------------------------------------------
        # Deals Closing Soon
        # -------------------------------------------------

        elif query_type == "closing_soon":

            st.subheader("Deals Closing Soon")

            st.dataframe(result)


        # -------------------------------------------------
        # Sector Analysis
        # -------------------------------------------------

        elif query_type == "sector_analysis":

            st.subheader("Pipeline Value by Sector")

            sector_value = pipeline_value_by_sector(df)

            st.dataframe(sector_value)

            fig, ax = plt.subplots()

            sector_value.plot(kind="bar", ax=ax)

            ax.set_title("Pipeline Value by Sector")

            st.pyplot(fig)


        # -------------------------------------------------
        # Revenue Forecast
        # -------------------------------------------------

        elif query_type == "revenue_forecast":

            forecast_df, summary = result

            st.subheader("Revenue Forecast")

            st.write(
                f"Expected Revenue: ₹{summary['expected_revenue']:,.0f}"
            )

            st.dataframe(forecast_df)


        # -------------------------------------------------
        # Default Pipeline Overview
        # -------------------------------------------------

        else:

            st.subheader("Pipeline Overview")

            st.write("Total Deals:", metrics["total_deals"])

            st.write(
                "Total Pipeline Value:",
                f"₹{metrics['total_pipeline_value']:,.0f}"
            )

            st.subheader("Deals by Sector")

            st.bar_chart(metrics["deals_by_sector"])

            st.subheader("Deals by Stage")

            st.bar_chart(metrics["deals_by_stage"])


        # -------------------------------------------------
        # AI Reasoning Panel
        # -------------------------------------------------

        with st.expander("AI Reasoning"):

            st.write("Detected Intent:", query_type)

            st.write("Analytics Module Used:", query_type)

            st.write("Data Source: Monday Deals Board")

            st.write("Records Analyzed:", len(df))


    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )


# -------------------------------------------------
# Footer
# -------------------------------------------------

st.markdown("---")

st.caption("AI Business Intelligence Agent powered by Monday.com data")