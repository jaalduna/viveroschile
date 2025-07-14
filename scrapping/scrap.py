import requests

import polars as pl
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_product_dataframe():
    base_url = "https://www.cincopinos.cl"

    # get cagegories

    categories = get_categories(base_url + "/collections")
    # categories = ["/colections/arboles"]

    results = {}
    for category in categories:
        current_page = 1
        while True:
            url = f"{base_url}{category}?page={current_page}"
            print(f"scraping page: {url} for category: {category}")

            try:
                result = scrape_page(url)
                if not result:
                    print(
                        f"No more products found on page {current_page} for category {category}."
                    )
                    break
                results = {**results, **result}
            except requests.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
            current_page += 1

    # save results to a polars df
    # save results
    with open("products.txt", "w", encoding="utf-8") as f:
        for description, price in results.items():
            f.write(f"{description}: {price}\n")

    result_list = [dict(item) for item in results.items()]
    df = pl.DataFrame(result_list)

    df.write_csv("products.csv", has_header=True, separator=";")
    df.write_parquet("products.parquet", has_header=True, separator=";")


def scrape_page(url):
    response = requests.get(url, headers=headers, timeout=10)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    item_selector = ".product-details"

    items = soup.select(item_selector)

    result = {}
    for item in items:
        description = item.select_one("span.title").get_text(strip=True)
        price = item.select_one("span.price").get_text(strip=True)
        result[description] = price
        print(f"Description: {description}, Price: {price}")

    return result


def get_categories(url):
    response = requests.get(url, headers=headers, timeout=10)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    item_selector = "a.collection-info__caption"

    items = soup.select(item_selector)

    categories = []
    for item in items:
        category = item.attrs.get("href", None)

        print(f"category: {category}")
        categories.append(category)

    assert len(categories) > 0, "No categories found on the page."
    return categories


def to_parquet(filename):
    with open(filename, "rb") as file:
        result = file.readlines()

    # parse each line and convert with the format <description>: <price>
    data = []
    for line in result:
        line = line.decode("utf-8").strip()
        if not line:
            continue
        description, price = line.split(": ")
        data.append({"description": description, "price": price})

    df = pl.DataFrame(data)
    df.write_parquet("results.parquet")


if __name__ == "__main__":
    get_product_dataframe()
    print("Scraping completed successfully.")
