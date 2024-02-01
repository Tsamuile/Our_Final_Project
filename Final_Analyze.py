#Importing necessary libraries for analyzing

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



# Reading data files

file1 = 'CSV files/Itaka_data.csv'
itaka = pd.read_csv(file1)
file2 = 'CSV files/Baltictours_data.csv'
baltic = pd.read_csv(file2)


#Change islands name to countries name and countries name to short country initials
itaka['Country'] = itaka['Country'].replace('Kanarų salos', 'Ispanija')
itaka['Country'] = itaka ['Country'].replace('Madeira', 'Portugalija')
itaka['Country'] = itaka['Country'].replace('Dominikos Respublika', 'Dominikos R.')
baltic['Country'] = baltic['Country'].replace('Dominikos Respublika', 'Dominikos R.')
itaka['Country'] = itaka['Country'].replace('Jungtiniai Arabų Emyratai', 'JAE')
itaka['Country'] = itaka['Country'].replace('Jungtinės Amerikos Valstijos', 'JAV')
baltic['Country'] = baltic['Country'].replace('Jungtinė Karalystė', 'UK')
itaka['Country'] = itaka['Country'].replace('Šiaurės Kipras', 'Š.Kipras')


# Preparing for 1 visualization :
# group by country and price average

itaka_average = itaka.groupby('Country')['Price'].mean().round(2)
baltic_average = baltic.groupby('Country')['Price'].mean().round(2)

#Creating horizontal bar

all_countries = itaka_average.index.union(baltic_average.index)
itaka_average = itaka_average.reindex(all_countries, fill_value=0)
baltic_average = baltic_average.reindex(all_countries, fill_value=0)
bar_width = 0.35
index = np.arange(len(all_countries))
plt.figure(figsize=(12, 8))

plt.barh(index, itaka_average, bar_width, label='Itaka', color='mediumpurple')
plt.barh(index + bar_width, baltic_average, bar_width, label='Baltic', color='teal')


plt.xlabel('Average Price (eur)')
plt.title('Compare Itaka and Baltictours directions by average price')

plt.yticks(index + bar_width / 2, all_countries, fontsize=10)
plt.legend()
plt.grid(True)
plt.show()

# Creating ID to calculate Top 5 countries by travel agencies offers

itaka['ID'] = range (1, 1 + len(itaka))
baltic['ID'] = range(1, 1 + len(baltic))

# Count total travels for each travel agency
itaka_total_travels = itaka['ID'].count()
baltic_total_travels = baltic['ID'].count()

itaka_top5 = itaka.groupby('Country')['ID'].count().sort_values(ascending=False).head(5)
baltic_top5 = baltic.groupby('Country')['ID'].count().sort_values(ascending=False).head(5)

# Preparing lists for pie chart (Itaka and Baltictours)
lab = itaka_top5.index
itaka_country_list = lab.tolist()
itaka_country_list.append('Kitos šalys')

itaka_travel_units = itaka_top5.tolist()
itaka_other_travel_units =itaka_total_travels - itaka_top5.sum()
itaka_travel_units.append(itaka_other_travel_units)

lab1 = baltic_top5.index
baltic_country_list = lab1.tolist()
baltic_country_list.append('Kitos šalys')

baltic_travel_units=baltic_top5.tolist()
baltic_other_travel_units =baltic_total_travels - baltic_top5.sum()
baltic_travel_units.append(baltic_other_travel_units)


#  Creating visualization to show top 5 countries for each travel agency by travel offers

palette_color = sns.color_palette('mako')
explode = [0.1, 0.1, 0, 0, 0, 0]
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 8))
axs[0].pie(itaka_travel_units, labels=itaka_country_list, colors=palette_color, explode=explode, autopct='%.0f%%')
axs[0].set_title('Itaka Top 5 countries offered')

explode1 = [0.0, 0.1, 0.1, 0, 0, 0]
axs[1].pie(baltic_travel_units, labels=baltic_country_list, colors=palette_color, explode = explode1,   autopct='%.0f%%')
axs[1].set_title('Baltic Top 5 countries offered')
plt.tight_layout()
plt.show()


# Greece and Spain deep analyze

# Itaka travel agency average price by duration in Greece and Spain
itaka['City'] = itaka['City'].replace('Malaga (Kosta del Solis)', 'Malaga')
itaka_Graikija = itaka[itaka['Country'] =='Graikija']
itaka_Graikija_group = itaka_Graikija.groupby('Duration')['Price'].mean().round(2)
itaka_Ispanija = itaka[itaka['Country'] =='Ispanija']
itaka_Ispanija_group = itaka_Ispanija.groupby('Duration')['Price'].mean().round(2)


# Baltictours travel agency average price by duration in Greece and Spain

baltic_Graikija = baltic[baltic['Country'] =='Graikija']
baltic_Graikija_group = baltic_Graikija.groupby('Duration')['Price'].mean().round(2)
baltic_Ispanija = baltic[baltic['Country'] =='Ispanija']
baltic_Ispanija_group = baltic_Ispanija.groupby('Duration')['Price'].mean().round(2)


# After analyze Greece data, found out both travel agencies offer almost the same trips on duration and price.
# Choose to analyze Spain cities by duration and average price.

baltic_result = baltic_Ispanija.groupby('City').aggregate({'Price':'mean','Duration':'mean'}).round(2)
itaka_result = itaka_Ispanija.groupby('City').aggregate({'Price':'mean','Duration':'mean'}).round(2)

#Checking correlation between price and duration
corr_itaka = itaka_Ispanija['Price'].corr(itaka_Ispanija['Duration']).round(2)
corr_baltic = baltic_Ispanija['Price'].corr(baltic_Ispanija['Duration']).round(2)


# Creating visualization to show Spain cities price and duration relationship (Itaka, Baltictours)

fig, axs = plt.subplots(1, 2, figsize=(15, 6))


sns.scatterplot(x=itaka_result['Duration'], y=itaka_result['Price'], ax=axs[0], color='mediumpurple', s=100)
axs[0].set_title('Itaka - Price vs Duration by Spain cities')
axs[0].set_xlabel('Average Duration (Days)')
axs[0].set_ylabel('Average Price (eur)')
axs[0].grid(True)
for i in range(len(itaka_result)):
    axs[0].text(itaka_result['Duration'].iloc[i] + 0.1, itaka_result['Price'].iloc[i] + 0.1,
                itaka_result.index[i], fontsize=9, ha='right')

sns.scatterplot(x=baltic_result['Duration'], y=baltic_result['Price'], ax=axs[1], color='teal', s=100)
axs[1].set_title('Baltic - Price vs Duration by Spain cities')
axs[1].set_xlabel('Average Duration (Days)')
axs[1].set_ylabel('Average Price (eur)')
axs[1].grid(True)
for i in range(len(baltic_result)):
    axs[1].text(baltic_result['Duration'].iloc[i] + 0.1, baltic_result['Price'].iloc[i] + 0.1,
                baltic_result.index[i], fontsize=9, ha='right')

plt.tight_layout()
plt.show()

# Analyze top 5 the most expensive travels by Itaka and Baltic

baltic_expensive = baltic.groupby('Country').aggregate({'Price':'max','Duration':'mean'}).round(2)
itaka_expensive = itaka.groupby('Country').aggregate({'Price':'max', 'Duration':'mean'}).round(2)
sort_itaka_expensive = itaka_expensive.sort_values(by=["Price"], ascending=False).head(5)
sort_baltic_expensive = baltic_expensive.sort_values(by=["Price"], ascending=False).head(5)

# Create bar visualization:
# to show the most expensive countries by offers to compare between Itaka and Baltictours(average price,duration)
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

sns.barplot(x=sort_itaka_expensive.index, y=sort_itaka_expensive['Price'], ax=axs[0, 0], color='mediumpurple')
axs[0, 0].set_title('Itaka - average price by TOP 5 most expensive countries ')
axs[0, 0].set_ylabel('Average Price (eur)')
axs[0, 0].tick_params(axis='x', rotation=45)

sns.barplot(x=sort_baltic_expensive.index, y=sort_baltic_expensive['Price'], ax=axs[0, 1], color='mediumpurple')
axs[0, 1].set_title('Baltictours - average price by TOP 5 most expensive countries ')
axs[0, 1].set_ylabel('Average Price (eur)')
axs[0, 1].tick_params(axis='x', rotation=45)

sns.barplot(x=sort_itaka_expensive.index, y=sort_itaka_expensive['Duration'], ax=axs[1, 0], color='teal')
axs[1, 0].set_title('Itaka - Average Duration by country')
axs[1, 0].set_ylabel('Average Duration (Days)')
axs[1, 0].tick_params(axis='x', rotation=45)

sns.barplot(x=sort_baltic_expensive.index, y=sort_baltic_expensive['Duration'], ax=axs[1, 1], color='teal')
axs[1, 1].set_title('Baltic - Average Duration by country')
axs[1, 1].set_ylabel('Average Duration (Days)')
axs[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()


