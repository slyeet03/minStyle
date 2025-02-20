from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def search(query, driver):
    """
    searches for a given query on amazon and extract product details

    parameters:
        query: the search query entered by the user
        driver: selenium webdriver instance

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

        return result(soup, name_elements, price_elements)

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

    finally:
        # closing the browser
        driver.quit()


def result(soup, name, price):
    """
    Extracts product data from the source code.

    Parameters:
        soup: BeautifulSoup object
        name: list of name elements
        price: list of price elements
        image: list of image elements

    Return: list of product data
    """
    links = []
    names = []
    prices = []
    image = []

    try:
        # Extract product names (picking top 18 results)
        for n in name[:18]:
            name_tag = n.find("span")
            names.append(name_tag.text.strip() if name_tag else "No Name")

        # Extract product prices (Ensuring all products have a price)
        price_dict = {
            p.find_parent("div", class_="a-section").find(
                "span", class_="a-price-whole"
            ): p.text.strip()
            for p in price
        }

        for i in range(len(names)):
            prices.append(
                price_dict.get(price[i], "N/A")
            )  # Default to "N/A" if price is missing

        # Extract product links
        for link in soup.find_all("a", class_="a-link-normal s-no-outline")[:18]:
            links.append("https://www.amazon.in" + link.get("href"))

        # Extract product image links
        for div in soup.find_all(
            "div", class_="a-section aok-relative s-image-tall-aspect"
        )[:18]:
            img_tag = div.find("img", class_="s-image")
            image.append(
                img_tag["src"] if img_tag and "src" in img_tag.attrs else "No Image"
            )

        return names, prices, links, image

    except Exception as e:
        print("Error in amazon_result:", e)
        return None, None, None, None
