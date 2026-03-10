from monday.client import run_query
from config import DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID


def fetch_board_items(board_id):

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        items_page(limit: 500) {{
          items {{
            name
            column_values {{
              id
              text
            }}
          }}
        }}
      }}
    }}
    """

    data = run_query(query)

    items = data["data"]["boards"][0]["items_page"]["items"]

    return items


def fetch_deals_board():
    return fetch_board_items(DEALS_BOARD_ID)


def fetch_workorders_board():
    return fetch_board_items(WORK_ORDERS_BOARD_ID)