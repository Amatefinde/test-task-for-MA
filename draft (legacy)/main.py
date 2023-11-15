import aiohttp
import asyncio
from bs4 import BeautifulSoup
from bs4.element import Tag
from time import time
from utils import urljoin
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
}


async def fetch_page(url, params=None, headers=None):
    headers = headers or HEADERS
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            return await response.text()


async def get_product_cards(url, batch_size) -> list[Tag]:
    i: int = 1
    is_finish = False
    product_cards = []
    while not is_finish:
        tasks = [fetch_page(url, params={"page": i + x}) for x in range(batch_size)]
        contents = await asyncio.gather(*tasks)
        for page in contents:
            soup = BeautifulSoup(page, "lxml")
            products = soup.findAll(class_="product-card")
            product_cards.extend(products)
            if not products:
                is_finish = True
        i += batch_size

    return product_cards


def get_product_paths(product_cards: list[Tag]) -> list[str]:
    product_paths = []
    for card in product_cards:
        product_path = card.find(attrs={"data-qa": True})["href"]
        product_paths.append(product_path)
    return product_paths


async def download_product_pages(base_url: str, paths: list[str]) -> tuple:
    product_urls = [urljoin(base_url, product_path) for product_path in paths]
    tasks = [fetch_page(url) for url in product_urls]
    contents = await asyncio.gather(*tasks)
    return contents


def parse_product_page(page: str):
    soup = BeautifulSoup(page, "lxml")

    title = soup.find(class_="product-page-content__product-name").text.strip()

    product_specs = soup.find(class_="style--product-page-full-list")
    brand_group = product_specs.find(text=re.compile(".*Бренд.*")).parent.parent.parent
    brand = brand_group.findAll("span")[-1].text.strip()
    print(title, brand, sep=", ")


async def main(base_url: str, category_path: str, batch_size: int):
    url = urljoin(base_url, category_path)
    product_cards: list[Tag] = await get_product_cards(url, batch_size)
    product_paths: list[str] = get_product_paths(product_cards)
    product_pages: tuple = await download_product_pages(base_url, product_paths)
    for page in product_pages:
        parse_product_page(page)


BATCH_SIZE = 10  # Number of pages that can be downloaded in one time
BASE_URL = "https://online.metro-cc.ru/"
CATEGORY_PATH = "category/ovoshchi-i-frukty/frukty"  # Link to category

if __name__ == "__main__":
    start = time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(BASE_URL, CATEGORY_PATH, BATCH_SIZE))
    print(time() - start)
