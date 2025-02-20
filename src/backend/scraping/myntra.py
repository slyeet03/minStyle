from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def search(query, driver):
    """
    Searches for a given query on Myntra and extracts product details.

    Parameters:
        query: The search query entered by the user.
        driver: Selenium WebDriver instance.

    Returns: lists of product names, prices, brands, links, and images.
    """
    url = f"https://www.myntra.com/shirt?rawQuery={query.replace(' ', '%20')}"

    try:
        driver.get(url)

        # Wait for products to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.product-base"))
        )

        # Parse the page source
        soup = bs(driver.page_source, "html.parser")

        # Extract all product containers
        product_containers = soup.find_all("li", class_="product-base")[:18]

        if not product_containers:
            print("No results found. Possible class name change.")
            return None, None, None, None, None  # Returning 5 None values

        return extract_product_data(product_containers)

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None, None, None

    finally:
        driver.quit()


def extract_product_data(product_containers):
    """
    Extracts product data from the parsed HTML.

    Parameters:
        product_containers: List of product elements (li.product-base)

    Returns: Lists of product names, prices, links, images, and brands.
    """
    base_url = "https://www.myntra.com"
    names, prices, links, images, brands = [], [], [], [], []

    try:
        for product in product_containers:
            # Extract product name
            name_tag = product.find("h4", class_="product-product")
            names.append(name_tag.text.strip() if name_tag else "No Name")

            # Extract brand name
            brand_tag = product.find("h3", class_="product-brand")
            brands.append(brand_tag.text.strip() if brand_tag else "No Brand Name")

            # Extract price
            price_tag = product.find("div", class_="product-price").find("span")
            prices.append(price_tag.text.strip() if price_tag else "N/A")

            # Extract product link
            link_tag = product.find("a", {"data-refreshpage": "true"})
            if link_tag and link_tag.get("href"):
                product_link = base_url + "/" + link_tag.get("href").lstrip("/")
                links.append(product_link)
            else:
                links.append("No Link")

            # Extract product image
            img_tag = product.find("img", class_="img-responsive")
            images.append(
                img_tag["src"] if img_tag and "src" in img_tag.attrs else "No Image"
            )

        return names, prices, links, images, brands

    except Exception as e:
        print("Error in extract_product_data:", e)
        return None, None, None, None, None  # Return 5 None values in case of error
