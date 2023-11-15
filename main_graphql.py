from typing import Any

import pandas as pd
import requests

from graphql_request import graphql_url, graphql_query, graphql_variables
from utils import urljoin

BASE_URL: str = "https://online.metro-cc.ru/"


def send_graphql_request(
    url: str, query: str, variables: dict[str, Any]
) -> dict[str, Any]:
    headers: dict[str, str] = {
        "Content-Type": "application/json",
    }
    data: dict[str, Any] = {"query": query, "variables": variables}
    response: requests.Response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


def save_to_excel(
    products: list[dict[str, Any]], filename: str = "output.xlsx"
) -> None:
    data: dict[str, list[Any]] = {
        "ID": [product["id"] for product in products],
        "Name": [product["name"] for product in products],
        "URL": [urljoin(BASE_URL, product["url"]) for product in products],
        "Manufacturer": [product["manufacturer"]["name"] for product in products],
        "Promo Price": [
            product["stocks"][0]["prices"]["price"]
            if product["stocks"][0]["prices"]["old_price"]
            else None
            for product in products
        ],
        "Base Price": [
            product["stocks"][0]["prices"]["old_price"]
            if product["stocks"][0]["prices"]["old_price"]
            else product["stocks"][0]["prices"]["price"]
            for product in products
        ],
        "amount": [product["stocks"][0]["value"] for product in products],
    }

    df: pd.DataFrame = pd.DataFrame(data)

    condition = df["amount"]
    df = df.drop(condition[condition == 0].index)
    df.drop("amount", axis=1, inplace=True)

    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")


def main() -> None:
    try:
        result: dict[str, Any] = send_graphql_request(
            graphql_url, graphql_query, graphql_variables
        )
        products: list[dict[str, Any]] = result["data"]["category"]["products"]
        save_to_excel(products)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
