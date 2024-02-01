# Importing necessary libraries for scraping website

from bs4 import BeautifulSoup
import requests
import pandas as pd

all_data = []
for i in range(1, 20):
    url = f'https://www.baltictours.lt/?month=-2&orderby=date&order=desc&taxonomy2&page={i}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = soup.find_all('div', class_='s2l-el special__offer')

    # Find necessary data from website

    for product in products:
        country = product.find('div', class_='country').text.strip()
        city = product.find('div', class_='city').text.strip()
        hotel_stars = product.find('div', class_='stars')
        if hotel_stars:
            class_name = hotel_stars.get('class')[1]
            Hotel_stars = class_name.split('-')[1]
        price_full = product.find('div', class_='price').text.strip().replace('€', '')
        date_nights = product.find('div', class_='date').text.strip()
        string = date_nights
        Date_only = string[:10]
        Nights_only = string[10:]
        title = product.find('div', class_='special__offer-description').text.strip()

        # Creating dictionary

        all_data.append({
            'Country': country,
            'City': city,
            'Price_Full': price_full,
            'Title': title,
            'Date': Date_only,
            'Night': Nights_only,
            'Hotel_stars': Hotel_stars
        })

# Inserting to DataFrame Pandas and changing data types, splitting columns and dropping not needed columns

df = pd.DataFrame(all_data)
df[['Nereikalinga_kaina', 'Price']] = df['Price_Full'].str.split(expand=True)
df['Price'] = df['Price'].astype(int)
df['Date'] = pd.to_datetime(df['Date'])
df[['Duration', 'Nereikia']] = df['Night'].str.split(expand=True)
df['Duration'] = df['Duration'].astype(int)
df['Hotel_stars'] = df['Hotel_stars'].astype(int)
df.drop(['Price_Full', 'Title', 'Night', 'Nereikalinga_kaina', 'Nereikia'], axis=1, inplace=True)

# Final step save as CSV file
df.to_csv('Baltictours_data.csv', index=False)
# print(df)
