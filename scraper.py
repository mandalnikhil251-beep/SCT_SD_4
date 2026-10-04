import requests
from bs4 import BeautifulSoup
import csv


URL = "https://books.toscrape.com/"


def scrape_products(url=URL):

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    rating_words = {
        "One": 1.0,
        "Two": 2.0,
        "Three": 3.0,
        "Four": 4.0,
        "Five": 5.0
    }

    gbp_to_inr = 115

    for book in soup.select("article.product_pod"):

        name = book.h3.a["title"]

        price_text = book.select_one(
            ".price_color"
        ).text.strip()

        price_number = "".join(
            character
            for character in price_text
            if character.isdigit() or character == "."
        )

        gbp_price = float(price_number)

        inr_price = gbp_price * gbp_to_inr

        price = f"₹{inr_price:,.2f}"

        rating_element = book.select_one(
            "p.star-rating"
        )

        rating_name = rating_element.get(
            "class",
            ["", "Not rated"]
        )[1]

        rating = rating_words.get(
            rating_name,
            0.0
        )

        products.append({
            "name": name,
            "price": price,
            "rating": rating
        })

    return products


def save_to_csv(products):

    with open(
        "products.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["name", "price", "rating"]
        )

        writer.writeheader()
        writer.writerows(products)


if __name__ == "__main__":

    products = scrape_products()

    save_to_csv(products)

    print(
        f"Successfully extracted {len(products)} products."
    )

    print("Data saved to products.csv")