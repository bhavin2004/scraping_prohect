from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# Initialize the WebDriver (Ensure you have the correct WebDriver installed)
driver = webdriver.Chrome()

# Open the first page
driver.get("https://books.toscrape.com/catalogue/page-45.html")

books = []
book_titles = []
page_no = 1

while True:
    # Extract book URLs and titles
    book_elements = driver.find_elements(By.CSS_SELECTOR, ".product_pod h3 a")
    for book in book_elements:
        books.append(book.get_attribute('href'))
        book_titles.append(book.text.strip())

    print(f"Scraped Page {page_no}")

    # Check if "Next" button exists
    try:
        next_button = driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
        next_button.click()
        time.sleep(1)  # Small delay to prevent excessive requests
        page_no += 1
    except Exception:
        print("Reached the last page. Stopping...")
        break

# Create directory for saving pages
os.makedirs("html_data1", exist_ok=True)

# Visit each book's page and save its HTML
for idx, book_url in enumerate(books):
    driver.get(book_url)
    with open(f"html_data1/book{idx+1}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

print(f"Scraped {len(book_titles)} books successfully!")
driver.quit()
