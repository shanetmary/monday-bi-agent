import requests
from config import MONDAY_API_TOKEN

API_URL = "https://api.monday.com/v2"

headers = {
    "Authorization": MONDAY_API_TOKEN,
    "Content-Type": "application/json"
}

def run_query(query):
    response = requests.post(
        API_URL,
        json={"query": query},
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.text}")

    return response.json()