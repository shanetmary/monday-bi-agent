import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def pipeline_summary(df):

    df["deal_value"] = pd.to_numeric(df["deal_value"], errors="coerce")

    total_pipeline_value = df["deal_value"].sum()

    total_deals = len(df)

    deals_by_sector = df["sector"].value_counts()

    deals_by_stage = df["deal_stage"].value_counts()

    return {
        "total_pipeline_value": total_pipeline_value,
        "total_deals": total_deals,
        "deals_by_sector": deals_by_sector,
        "deals_by_stage": deals_by_stage
    }


def deals_closing_soon(df):

    df["tentative_close_date"] = pd.to_datetime(
        df["tentative_close_date"], errors="coerce"
    )

    today = datetime.today()

    next_30_days = today + timedelta(days=30)

    closing = df[
        (df["tentative_close_date"] >= today)
        &
        (df["tentative_close_date"] <= next_30_days)
    ]

    return closing[
        [
            "deal_name",
            "client_code",
            "deal_value",
            "tentative_close_date",
            "deal_stage",
        ]
    ]


def top_deals(df):

    df["deal_value"] = pd.to_numeric(df["deal_value"], errors="coerce")

    top = df.sort_values("deal_value", ascending=False)

    return top[
        [
            "deal_name",
            "client_code",
            "deal_value",
            "sector"
        ]
    ].head(5)


def detect_anomalies(df):

    anomalies = []

    missing_sector = df["sector"].isna().sum()
    missing_value = df["deal_value"].isna().sum()
    missing_close = df["tentative_close_date"].isna().sum()

    if missing_sector > 0:
        anomalies.append(
            f"{missing_sector} deals have missing sector information"
        )

    if missing_value > 0:
        anomalies.append(
            f"{missing_value} deals have missing deal values"
        )

    if missing_close > 0:
        anomalies.append(
            f"{missing_close} deals have missing close dates"
        )

    return anomalies


def detect_risky_deals(df):

    df["tentative_close_date"] = pd.to_datetime(
        df["tentative_close_date"], errors="coerce"
    )

    today = datetime.today()

    risky = df[
        (df["tentative_close_date"] < today)
        &
        (df["deal_stage"] != "Project Won")
    ]

    return risky[
        [
            "deal_name",
            "client_code",
            "deal_value",
            "tentative_close_date",
            "deal_stage"
        ]
    ]


def pipeline_bottlenecks(metrics):

    stage_counts = metrics["deals_by_stage"]

    bottleneck_stage = stage_counts.idxmax()

    bottleneck_count = stage_counts.max()

    return bottleneck_stage, bottleneck_count


def pipeline_value_by_sector(df):

    df["deal_value"] = pd.to_numeric(df["deal_value"], errors="coerce")

    sector_value = df.groupby("sector")["deal_value"].sum()

    sector_value = sector_value.sort_values(ascending=False)

    return sector_value


# -------------------------------------------------
# Pipeline Funnel Chart
# -------------------------------------------------

def pipeline_funnel_chart(df):

    stage_counts = df["deal_stage"].value_counts()

    fig, ax = plt.subplots()

    ax.bar(stage_counts.index, stage_counts.values)

    ax.set_title("Sales Pipeline Funnel")

    ax.set_xlabel("Deal Stage")

    ax.set_ylabel("Number of Deals")

    plt.xticks(rotation=45)

    return fig