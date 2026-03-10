import pandas as pd
from datetime import datetime


def calculate_deal_health(df):

    df = df.copy()

    today = pd.Timestamp.today()

    health_scores = []

    for _, row in df.iterrows():

        score = 100

        # Missing sector
        if pd.isna(row.get("sector")) or row.get("sector") == "":
            score -= 15

        # Missing deal value
        if pd.isna(row.get("deal_value")):
            score -= 20

        # Missing close date
        close_date = row.get("close_date")

        if pd.isna(close_date):
            score -= 15

        else:
            if close_date < today:
                score -= 30

        # Stage risk
        stage = str(row.get("stage", "")).lower()

        if "lead" in stage or "qualification" in stage:
            score -= 5

        if "proposal" in stage:
            score -= 10

        # Ensure score stays within range
        score = max(score, 0)

        health_scores.append(score)

    df["deal_health_score"] = health_scores

    return df


def get_risky_deals(df):

    df = calculate_deal_health(df)

    risky = df[df["deal_health_score"] < 60]

    return risky.sort_values("deal_health_score")


def get_healthy_deals(df):

    df = calculate_deal_health(df)

    healthy = df[df["deal_health_score"] >= 80]

    return healthy.sort_values("deal_health_score", ascending=False)