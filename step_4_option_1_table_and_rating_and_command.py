import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

import html_url
import os
import sys
sys.path.append("/home/seam/SEAM/CODE/")


# import html_url
html_1 = html_url.url_html


def setup_driver():
    """Set up Chrome WebDriver."""
    options = Options()
    options.headless = False  # Run Chrome with a visible browser window
    service = Service(
        "/usr/bin/chromedriver"
    )  # Update with the path to your chromedriver executable
    return webdriver.Chrome(service=service, options=options)


def scroll_page(driver, scroll_amount, sleep_time=5):
    """Scroll the page by the given amount."""
    print(scroll_amount)
    driver.execute_script("window.scrollBy(0, {})".format(scroll_amount))
    time.sleep(sleep_time)


def extract_table_content(driver, url):
    """Extract table content and header from the page."""
    try:
        scroll_amounts = [20000, -10000, 5000, -1000, -
                          100, -100, -100, 100, 100, 100, 100, 100, 100, 100]

        for scroll_amount in scroll_amounts:
            scroll_page(driver, scroll_amount)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(5)  # Add a small delay to ensure all content is loaded

        # Extract table content
        page_html = driver.page_source
        # page_html=html_1 #use when page is not load properlyu
        soup = BeautifulSoup(page_html, "html.parser")

        table_body = soup.find('body')
        print(table_body)
        if table_body:
            # Extract table header
            table_header = [th.text.strip()
                            for th in soup.find('thead').find_all('th')]
            print("=========table_header=========")
            print(table_header)
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

            print("======title=========")
            print(title)

            # Extracting general description
            general_description = soup.find(
                'div', class_='commentItem-mainText').text.strip()

            print("======general_description=========")
            print(general_description)

            # Extracting itemization
            itemization_list = soup.find_all(
                'li', class_='articleFeaturesItem')
            itemization = [item.text.strip() for item in itemization_list]

            print("======itemization_list=========")
            print(itemization_list)

            # ====================ratting===============
            rating_span = soup.find(
                'span', class_='BVRRNumber BVRRRatingNumber')
            rating = rating_span.text.strip() if rating_span else None
            print("======rating_span=========")
            print(rating_span)
            num_reviews_span = soup.find(
                'span', class_='BVRRNumber BVRRBuyAgainTotal')
            print("======num_reviews_span=========")
            print(num_reviews_span)
            num_reviews = num_reviews_span.text.strip() if num_reviews_span else None

            recommended_rate_span = soup.find(
                'span', class_='BVRRNumber BVRRBuyAgainRecommend')
            print("======recommended_rate_span=========")
            print(recommended_rate_span)
            recommended_rate = recommended_rate_span.text.strip() if recommended_rate_span else None

            # ===========================kws
            keyword_links = soup.find_all('div', class_='itemTagsPosition')
            print("======keyword_links=========")
            print(keyword_links)

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
    except Exception as e:
        print(f"Error extracting table content: {str(e)}")
    return {"table_header": [], "table_data": [], "url": url}


def main(urls):
    # Set up WebDriver
    driver = setup_driver()

    all_data = []
    for url in urls:
        driver.get(url)
        table_data = extract_table_content(driver, url)
        if table_data['size_information_data']:
            all_data.append(table_data)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv('table_data.csv', index=False)
        print("Table data saved to table_data.csv")
        print(urls)
    # Close the WebDriver session
    driver.quit()


if __name__ == "__main__":
    df = pd.read_csv('dis_man_1_href.csv')
    urls = df['complete_url'].tolist()
    # urls = [
    #     "https://shop.adidas.jp/products/IU0210/",
    #     "https://shop.adidas.jp/products/IC8391/",
    #     "https://shop.adidas.jp/products/IP0418/",
    # ]
    main(urls)
