import pandas as pd


def build_deals_dataframe(items):

    rows = []

    for item in items:

        values = [col["text"] for col in item["column_values"]]

        row = {
            "deal_name": item["name"],
            "owner_code": values[0],
            "client_code": values[1],
            "deal_status": values[2],
            "close_date": values[3],
            "closure_probability": values[4],
            "deal_value": values[5],
            "tentative_close_date": values[6],
            "deal_stage": values[7],
            "product": values[8],
            "sector": values[9],
            "created_date": values[10],
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    return df