import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def setup_driver():
    """Set up Chrome WebDriver."""
    options = Options()
    options.headless = False  # Run Chrome with a visible browser window
    service = Service('/usr/bin/chromedriver')  # Update with the path to your chromedriver executable
    return webdriver.Chrome(service=service, options=options)

def scroll_page(driver, scroll_amount, sleep_time=15):
    """Scroll the page by the given amount."""
    driver.execute_script("window.scrollBy(0, {})".format(scroll_amount))
    time.sleep(sleep_time)
    print(scroll_amount)

def extract_table_content(driver, url):
    """Extract table content and header from the page."""
    try:
        # Scroll the page to load content
        scroll_page(driver, 20000)

        # Scroll up to load more content if necessary
        scroll_page(driver, -10000)

        # Scroll again to ensure all content is loaded
        scroll_page(driver, 5000)
        scroll_page(driver, -1000)
        scroll_page(driver, 1000)
        scroll_page(driver, -500)
        scroll_page(driver, 500)
        scroll_page(driver, -500)
        scroll_page(driver, 500)
        scroll_page(driver, -500)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-zn7duo')))
        time.sleep(5)  # Add a small delay to ensure all content is loaded

        # Extract table content
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')
        table_body = soup.find('tbody')
        if table_body:
            # Extract table header
            table_header = [th.text.strip() for th in soup.find('thead').find_all('th')]
            # Extract table data
            rows = table_body.find_all('tr')
            table_data = [[cell.text.strip() for cell in row.find_all('td')] for row in rows]
            return {'table_header': table_header, 'table_data': table_data, 'url': url}
        else:
            print("Table body not found.")
    except Exception as e:
        print(f"Error extracting table content: {str(e)}")
    return {'table_header': [], 'table_data': [], 'url': url}

def main(urls):
    # Set up WebDriver
    driver = setup_driver()

    all_data = []
    for url in urls:
        driver.get(url)
        table_data = extract_table_content(driver, url)
        if table_data['table_data']:
            all_data.append(table_data)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv('table_data.csv', index=False)
        print("Table data saved to table_data.csv")

    # Close the WebDriver session
    driver.quit()

if __name__ == "__main__":
    urls = [
        "https://shop.adidas.jp/products/IU0210/",
        "https://shop.adidas.jp/products/IC8391/",
        "https://shop.adidas.jp/products/IP0418/"
    ]
    main(urls)
