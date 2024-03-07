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
    options.headless = True  # Run Chrome in headless mode, comment this line to see the browser window
    service = Service('/usr/bin/chromedriver')  # Update with the path to your chromedriver executable
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

def main(urls):
    # Set up WebDriver
    driver = setup_driver()

    all_data = []

    for url in urls:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        # Get the HTML content of the entire page
        page_html = driver.page_source
        # Pass the HTML content to BeautifulSoup for parsing
        soup = BeautifulSoup(page_html, 'html.parser')

        try:
            # Extract data
            breadcrumb = '/'.join([item.text.strip() for item in soup.select('.breadcrumbListItem a')])
            category = '/'.join([item.text.strip() for item in soup.select('.groupName .categoryName')])
            product_name_element = soup.find(class_='articleNameHeader').find('h1')
            product_name = product_name_element.text.strip() if product_name_element else None
            pricing = soup.find(class_='price-value').text.strip()
            available_sizes = ', '.join([item.text.strip() for item in soup.select('.sizeSelectorListItemButton')])
        except Exception as e:
            print(f"Error extracting data from {url}: {e}")
            continue  # Skip to the next URL

        # Create DataFrame
        data = {
            'Breadcrumb(Category)': [breadcrumb],
            'Category': [category],
            'Product name': [product_name],
            'Pricing': [pricing],
            'Available size': [available_sizes],
            'url':[url]
        }

        all_data.append(data)

    # Concatenate all data into a single DataFrame
    final_data = pd.concat([pd.DataFrame(data) for data in all_data], ignore_index=True)

    # Save to CSV
    save_to_csv(final_data)

    # Close the WebDriver session
    driver.quit()

    # Set up WebDriver
    driver = setup_driver()

    all_data = []

    for url in urls:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        # Get the HTML content of the entire page
        page_html = driver.page_source
        # Pass the HTML content to BeautifulSoup for parsing
        soup = BeautifulSoup(page_html, 'html.parser')

        # Extract data
        breadcrumb = '/'.join([item.text.strip() for item in soup.select('.breadcrumbListItem a')])
        category = '/'.join([item.text.strip() for item in soup.select('.groupName .categoryName')])
        product_name = soup.find(class_='articleNameHeader').find('h1').text.strip()
        pricing = soup.find(class_='price-value').text.strip()
        available_sizes = ', '.join([item.text.strip() for item in soup.select('.sizeSelectorListItemButton')])

        # Create DataFrame
        data = {
            'Breadcrumb(Category)': [breadcrumb],
            'Category': [category],
            'Product name': [product_name],
            'Pricing': [pricing],
            'Available size': [available_sizes],
            'url':[url]
        }

        all_data.append(data)

    # Concatenate all data into a single DataFrame
    final_data = pd.concat([pd.DataFrame(data) for data in all_data], ignore_index=True)

    # Save to CSV
    save_to_csv(final_data)

    # Close the WebDriver session
    driver.quit()

if __name__ == "__main__":
    df = pd.read_csv('dis_man_1_href.csv')

    # # Extract the URLs from the 'complete_url' column
    urls = df['complete_url'].tolist()
    # urls = [
    #     "https://shop.adidas.jp/products/IU0210/",
    #     "https://shop.adidas.jp/products/IC8391/"
    # ]
    main(urls)
