import html_url
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import sys
sys.path.append("/home/seam/SEAM/CODE/")


# import html_url
html_1 = html_url.url_html


# def setup_driver():
#     """Set up Firefox WebDriver with Tor proxy."""
#     tor_proxy = "127.0.0.1:9050"  # Tor proxy address

#     firefox_options = Options()
#     firefox_options.headless = False  # Run Firefox with a visible browser window
#     # Ignore SSL certificate errors
#     firefox_options.add_argument('--ignore-certificate-errors')
#     firefox_options.add_argument('--ignore-ssl-errors')  # Ignore SSL errors
#     firefox_options.add_argument('--no-sandbox')  # Bypass OS security model
#     firefox_options.add_argument(
#         '--disable-dev-shm-usage')  # Disable /dev/shm usage
#     # Disable GPU usage (useful for headless mode)
#     firefox_options.add_argument('--disable-gpu')

#     # Configure Tor proxy in Firefox preferences
#     firefox_profile = webdriver.FirefoxProfile()
#     firefox_profile.set_preference('network.proxy.type', 1)
#     firefox_profile.set_preference('network.proxy.socks', '127.0.0.1')
#     firefox_profile.set_preference('network.proxy.socks_port', 9050)
#     firefox_profile.update_preferences()

#     firefox_options.profile = firefox_profile

#     # Update with the path to your geckodriver executable
#     service = Service('/usr/local/bin/geckodriver')
#     driver = webdriver.Firefox(service=service, options=firefox_options)
#     return driver


def extract_table_content(url):
    """Extract table content and header from the page."""
    max_attempts = 3  # Maximum number of attempts to extract table content
    attempt = 0
    while attempt < max_attempts:
        try:
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'table-class')))
            # time.sleep(5)  # Add a small delay to ensure all content is loaded
            page_html = html_1
            soup = BeautifulSoup(page_html, 'html.parser')
            table_body = soup.find('body')
            if table_body:
                # Extract table header
                table_header = [th.text.strip()
                                for th in soup.find('thead').find_all('th')]
                # Extract table data
                rows = table_body.find_all('tr')
                table_data = []
                for row in rows:
                    cells = row.find_all('td')
                    row_data = [cell.text.strip() for cell in cells]
                    table_data.append(row_data)
                # ==================discriptiopn==========
                # Extracting title
                title = soup.find('h2', class_='itemName').text.strip()

                # Extracting general description
                general_description = soup.find(
                    'div', class_='commentItem-mainText').text.strip()

                # Extracting itemization
                itemization_list = soup.find_all(
                    'li', class_='articleFeaturesItem')
                itemization = [item.text.strip() for item in itemization_list]

                # ====================ratting===============
                rating_span = soup.find(
                    'span', class_='BVRRNumber BVRRRatingNumber')
                rating = rating_span.text.strip() if rating_span else None

                num_reviews_span = soup.find(
                    'span', class_='BVRRNumber BVRRBuyAgainTotal')
                num_reviews = num_reviews_span.text.strip() if num_reviews_span else None

                recommended_rate_span = soup.find(
                    'span', class_='BVRRNumber BVRRBuyAgainRecommend')
                recommended_rate = recommended_rate_span.text.strip() if recommended_rate_span else None

                # ===========================kws
                keyword_links = soup.find_all('div', class_='itemTagsPosition')

                # Extracting keywords from links
                keywords = [link.text.strip() for link in keyword_links]

                # Joining the keywords into a single string
                keywords_string = ' '.join(keywords)

                return {
                    'url': url,
                    'title_of_description': title,
                    'general_description_of_the_product': general_description,
                    'General_description(itemization)': itemization,
                    'size_information_table_header': table_header,
                    'size_information_data': table_data,
                    'Rating': rating,
                    'Number of Reviews': num_reviews,
                    'Recommended rate': recommended_rate,
                    "keywords": keywords_string
                }
            else:
                print("Table body not found.")
                attempt += 1
                print(f"Retrying ({attempt}/{max_attempts})...")
                time.sleep(2)  # Add a delay before retrying
        except Exception as e:
            print(f"Error extracting table content: {str(e)}")
            attempt += 1
            print(f"Retrying ({attempt}/{max_attempts})...")
            time.sleep(2)  # Add a delay before retrying
    print("Max attempts reached. Failed to extract table content.")
    return {'url': url, 'size_information_table_header': [], 'size_information_data': []}


def main(urls):
    # Set up WebDriver
    # driver = setup_driver()

    all_data = []
    for url in urls:
        # driver.get(url)
        table_data = extract_table_content(url)
        if table_data['size_information_data']:
            all_data.append(table_data)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv('table_data.csv', index=False, mode='a',
                  header=not os.path.exists('table_data.csv'))
        print("Table data saved to table_data.csv")
        print(urls)

    # Close the WebDriver session
    # driver.quit()


if __name__ == "__main__":
    urls = [
        "https://shop.adidas.jp/products/IC8391/"
    ]
    main(urls)
