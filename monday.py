import requests

MONDAY_API_URL = "https://api.monday.com/v2"


def run_monday_query(api_key, query):
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query},
        headers=headers
    )

    return response.json()
