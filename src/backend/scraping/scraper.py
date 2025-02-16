import platform
import time

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Detect OS
os_name = platform.system()

if os_name == "Windows":
    from selenium.webdriver.edge.options import Options

    options = Options()
    options.add_argument(
        "--headless"
    )  # running the browser without appearing on screen
    options.add_argument("--disable-gpu")

    driver = webdriver.Edge(options=options)

elif os_name == "Darwin":  # macOS\
    # safari does not support headless mode
    driver = webdriver.Safari()

else:
    raise Exception(
        "Unsupported OS. This script supports Windows (Edge) and macOS (Safari)."
    )


def amazon_search(query):
    """
    searches for a given query on amazon and extract product details

    parameters:
        query: the search query entered by the user

    return: list of product names, prices and links
    """
    url = "https://www.amazon.in/s?k=" + query

    try:
        driver.get(url)

        # Wait for the first product link to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal",
                )
            )
        )

        # parse the source code of the webpage
        soup = bs(driver.page_source, "html.parser")

        # finding name and price elements
        name_elements = soup.find_all(
            "a", class_="a-link-normal s-line-clamp-2 s-link-style a-text-normal"
        )

        price_elements = soup.find_all("span", class_="a-price-whole")

        if not name_elements or not price_elements:
            print("No results found. Possible class name change.")
            return None, None, None  # Avoid unpacking NoneType

        return amazon_result(soup, name_elements, price_elements)

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

    finally:
        # closing the browser
        driver.quit()


def amazon_result(soup, name, price):
    """
    extracts the product data from the source code

    parameters:
        soup: BeautifulSoup object
        name: list of name elements
        price: list of price elements

    return: list of product data
    """
    links = []
    name_content = []
    price_content = []

    try:
        # extract product name and prices (picking top 18 results)
        for n, p in zip(name[:18], price[:18]):
            name = n.find("span")
            if name:
                name_content.append(name.text.strip())

            price_content.append(p.text.strip())

        # extract product links (picking top 18 results)
        for link in soup.find_all("a", class_="a-link-normal s-no-outline")[:18]:
            links.append("https://www.amazon.in" + link.get("href"))

        return name_content, price_content, links

    except Exception as e:
        print("Error in amazon_result:", e)
        return None, None, None


# Get user input
query = input("Enter query: ")

name, price, links = amazon_search(query)

# display the results
if name and price and links:
    for i, (n, p, l) in enumerate(zip(name, price, links), start=1):
        print(f"{i}. {n} - ₹{p}\n{l}\n")
else:
    print("No valid results found.")

driver.quit()
