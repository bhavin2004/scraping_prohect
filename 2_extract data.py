import pandas as pd
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


# Extract book data
def extract_data(file):
    with open(f"html_data/{file}", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        book_title = soup.find("div", class_="product_main").h1.text.strip()
        book_price = soup.find("p", class_="price_color").text.strip()
        book_desc = soup.find_all("p")[3].text.strip()

        return [book_title, book_price, book_desc]
    #asbdhiahd

# Get all book files
books_path_list = os.listdir("html_data1/")
data = []

# Use ThreadPoolExecutor to speed up extraction
with ThreadPoolExecutor(max_workers=5) as executor:
    data = list(executor.map(extract_data, books_path_list))

# Save to CSV
df = pd.DataFrame(data, columns=["Name", "Price", "Description"])
df.to_csv("data.csv", index=False)

print(f"Data extraction complete! {len(data)} books saved to data.csv")
