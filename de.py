from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Initialize WebDriver (Single Instance)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Headless mode for performance
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()


start=time.time()
# Function to scrape all book URLs
def scrape_books():
    driver.get("https://books.toscrape.com/catalogue/page-1.html")

    books = []
    page_no = 1

    while True:
        # Extract book links
        book_elements = driver.find_elements(By.CSS_SELECTOR, ".product_pod h3 a")
        books.extend([book.get_attribute("href") for book in book_elements])
        
        print(f"Scraped Page {page_no}")

        # Check for "Next" button
        try:
            next_button = driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
            next_button.click()
            time.sleep(1)  # Allow page to load
            page_no += 1
        except:
            print("Reached last page. Stopping...")
            break

    return books

# Function to save a single book page (Runs in threads)
def save_book_page(window, book_id):
    driver.switch_to.window(window)  # Switch to tab
    time.sleep(1)  # Ensure page loads fully
    
    os.makedirs("html_data", exist_ok=True)
    with open(f"html_data/book{book_id}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    driver.close()  # Close tab after saving

# Function to process books in batches
def process_books_in_batches(books, batch_size=5):
    total_books = len(books)
    for i in range(0, total_books, batch_size):
        batch = books[i : i + batch_size]  # Get a batch of books
        print(f"\nProcessing batch {i//batch_size + 1}/{(total_books//batch_size)+1}")

        # Open batch of book tabs
        for book_url in batch:
            driver.execute_script(f"window.open('{book_url}');")
            time.sleep(0.5)  # Allow each tab to load

        # Multi-threading for saving pages
        windows = driver.window_handles[1:]  # Get new book tabs
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            for j, window in enumerate(windows):
                executor.submit(save_book_page, window, i + j + 1)

        driver.switch_to.window(driver.window_handles[0])  # Return to main tab

# Main Execution
if __name__ == "__main__":
    books = scrape_books()
    process_books_in_batches(books, batch_size=15)  # Process in batches
    driver.quit()
    print(time.time()-start)
    print(f"Scraped and saved {len(books)} book pages successfully!")
