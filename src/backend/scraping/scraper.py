import amazon
import util

# Get user input
query = input("Enter query: ")

driver = util.openBrowser()

# Extract product data
names, prices, links, images = amazon.search(query, driver)

# Store results in JSON if valid data is found
if names and prices and links and images:
    product_data = {
        f"P{i+1}": {"name": n, "price": f"₹{p}", "link": l, "image": img}
        for i, (n, p, l, img) in enumerate(zip(names, prices, links, images))
    }

    util.storeInJson("amazon", **product_data)

driver.quit()
