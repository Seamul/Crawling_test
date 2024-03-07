import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def setup_driver():
    """Set up Chrome WebDriver."""
    options = Options()
    # Run Chrome in headless mode, comment this line to see the browser window
    options.headless = True
    # Update with the path to your chromedriver executable
    service = Service('/usr/bin/chromedriver')
    return webdriver.Chrome(service=service, options=options)


def extract_product_details(soup):
    """Extract product details from BeautifulSoup object."""
    # Find all product items
    product_items = soup.find_all('div', class_='mt-merch-item')

    # Initialize lists to store product details
    titles = []
    prices = []
    image_urls = []

    # Iterate over each product item and extract details
    for item in product_items:
        # Extract product details
        title = item.find('div', class_='mt-title').text.strip()
        price = item.find('span', class_='mt-price').text.strip()
        image_url = item.find('img', class_='mt-image')['src']

        # Append details to lists
        titles.append(title)
        prices.append(price)
        image_urls.append(image_url)

    return titles, prices, image_urls


def save_to_csv(data, filename='product_details.csv'):
    """Save DataFrame to CSV."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Product details saved to {filename}")


def main():
    # Set up WebDriver
    driver = setup_driver()

    base_url = "https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops&page={}"

    # Initialize lists to store data
    href_list = []
    src_list = []

    # Loop through each page
    for page_num in range(1, 9):  # Adjust range based on the number of pages
        url = base_url.format(page_num)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Get the HTML content of the entire page
        page_html = driver.page_source
        # Pass the HTML content to BeautifulSoup for parsing
        soup = BeautifulSoup(page_html, 'html.parser')

        # Find all <a> tags with href containing '/products/'
        product_links = soup.find_all(
            'a', href=lambda href: href and '/products/' in href)

        # Extract href and src attributes
        for link in product_links:
            href = link.get('href')
            img_src = link.find('img').get('src')
            href_list.append(href)
            src_list.append(img_src)

    # Create a DataFrame
    data = {'href': href_list, 'src': src_list}
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv('dis_man.csv', index=False)

    print("Data saved to dis_man.csv")


def main():
    # Set up WebDriver
    driver = setup_driver()

    base_url = "https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops&page={}"

    # Initialize lists to store data
    href_list = []
    src_list = []

    # Loop through each page
    for page_num in range(1, 40):  # Adjust range based on the number of pages
        url = base_url.format(page_num)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        # Get the HTML content of the entire page
        page_html = driver.page_source
        # Pass the HTML content to BeautifulSoup for parsing
        soup = BeautifulSoup(page_html, 'html.parser')

        # Find all <a> tags with href containing '/products/'
        product_links = soup.find_all(
            'a', href=lambda href: href and '/products/' in href)

        # Extract href and src attributes
        for link in product_links:
            href = link.get('href')
            img_src = link.find('img').get('src')
            href_list.append(href)
            src_list.append(img_src)

    # Create a DataFrame
    data = {'href': href_list, 'src': src_list}
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv('dis_man_1.csv', index=False)

    print("Data saved to dis_man.csv")


if __name__ == "__main__":
    main()
