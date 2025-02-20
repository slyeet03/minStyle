import amazon
import myntra
import util

# Get user input
query = input("Enter query: ")

driver = util.openBrowser()

# Extract product data
names, prices, links, images, brands = myntra.search(query, driver)

# Store results in JSON if valid data is found
if names and prices and links and images and brands:
    product_data = {
        f"P{i+1}": {"name": n, "price": f"₹{p}", "link": l, "image": img, "brand": b}
        for i, (n, p, l, img, b) in enumerate(zip(names, prices, links, images, brands))
    }

    util.storeInJson("myntra", **product_data)

driver.quit()
