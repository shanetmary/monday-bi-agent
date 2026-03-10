import pandas as pd


STAGE_PROBABILITY = {
    "lead": 0.2,
    "qualification": 0.35,
    "proposal": 0.6,
    "negotiation": 0.8,
    "closed won": 1.0
}


def pipeline_forecast(df):

    df = df.copy()

    probabilities = []

    for _, row in df.iterrows():

        stage = str(row.get("stage", "")).lower()

        prob = 0.3  # default probability

        for key in STAGE_PROBABILITY:
            if key in stage:
                prob = STAGE_PROBABILITY[key]

        probabilities.append(prob)

    df["close_probability"] = probabilities

    df["expected_revenue"] = df["deal_value"] * df["close_probability"]

    forecast_summary = {
        "total_pipeline_value": df["deal_value"].sum(),
        "expected_revenue": df["expected_revenue"].sum(),
        "average_probability": df["close_probability"].mean()
    }

    return df, forecast_summary