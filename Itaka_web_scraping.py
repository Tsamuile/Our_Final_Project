# Importing necessary libraries for scraping website

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

# Website for scraping

target = [
    'https://www.itaka.lt/paieskos-rezultatai/?view=offerList&adults=2&date-from=2024-03-01&date-to=2024-05-31&total-price=0&currency=EUR']


# Function for newsletter
def close_newsletter(driver):
    try:
        # Waiting for newsletter pop-up
        newsletter_close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.sender-form-input-dB1gQb"))
        )
        newsletter_close_button.click()
    except TimeoutException:
        # If not appear in 10 second, continue code
        pass


# Function for load more button
def click_load_more(driver):
    try:
        load_more = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.offer-list_more-offers'))
        )
        driver.execute_script("arguments[0].click();", load_more)
        time.sleep(3)
    except (TimeoutException, ElementClickInterceptedException):

        print("Load More button was not clickable. Retrying...")
        time.sleep(3)
        click_load_more(driver)


# Function for scraping
def scrape_travels_data():
    table_data = []
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)

    for index, url in enumerate(target):
        driver.get(url)
        driver.maximize_window()
        time.sleep(5)

        for _ in range(12):
            # Before and after clicking "Load More" button, closing pop-up window
            close_newsletter(driver)
            click_load_more(driver)
            close_newsletter(driver)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        travels = soup.find_all('div', class_='offer_column offer_column-second col-sm-7 col-lg-8 clearfix')

        # Find necessary data from website

        for travel in travels:
            Hotel_name = travel.find('h2', class_='header_title').text.strip()
            Country_City = travel.find('div', class_='header_geo-labels').text.strip()
            Price = travel.find('span', class_='current-price_value').text.strip()
            Date_duration = travel.find('div', class_='offer_date hidden-xs pull-right').text.strip()
            Hotel_stars = travel.find('span', class_='header_stars')
            if Hotel_stars:
                class_name = Hotel_stars.get('class')[1]
                rating = class_name.split('-')[1].replace('0', '')

                # Creating dictionary

            table_data.append({
                'Hotel_name': Hotel_name,
                'Country_City': Country_City,
                'Price': Price,
                'Date_duration': Date_duration,
                'Hotel_stars': rating
            })

    driver.quit()
    return table_data


data = scrape_travels_data()

# Inserting to DataFrame Pandas and changing data types, splitting columns and dropping not needed columns
df = pd.DataFrame(data)
df[['Country', 'City']] = df['Country_City'].str.split(' / ', expand=True)
df['City'] = df['City'].fillna(' ')
df[['Date_weekday', 'Duration']] = df['Date_duration'].str.split('(', expand=True)
df['Duration'] = df['Duration'].str.replace('nakvynės)', '').astype(int)
df[['weekday', 'Date']] = df['Date_weekday'].str.split(expand=True)
df['Date'] = pd.to_datetime(df['Date'])
df['Price'] = df['Price'].str.replace(' ', '').astype(int)
df['Hotel_stars'] = df['Hotel_stars'].astype(int)
df.drop(['Country_City', 'Date_duration', 'Date_weekday', 'weekday'], axis=1, inplace=True)

# Final step save as CSV file

# df.to_csv('Itaka_data.csv', index=False)
# print(df)