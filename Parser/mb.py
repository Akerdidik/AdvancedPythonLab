from statistics import mean
from matplotlib.pyplot import title
from more_itertools import first_true
from numpy import angle, block, rot90
import requests
from bs4 import BeautifulSoup  as bs
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np




URL_popular = "https://animedao.to/animelist/popular" # URL for top anime list.

r_popular = requests.get(URL_popular)

soup_popular = bs(r_popular.content,'html.parser')



raw_data = [] # raw data: anime title, year of release and rating
name = [] # list with anime titles only
rate_list = [] # list with the rating of the anime 
links = [] # list with links to animes
genres_list = [] # list with anime genre



top_animes = soup_popular.findAll('div',class_='animeinfo')
for anime in top_animes:
    # alt = anime.find('div',class_='animeinfo_top h-100').find('p',class_='animetitle').text # anime title aliases
    # animename = anime.find('div',class_='animeinfo_top h-100').find('span',class_='animename').text  # title of the anime
    # rating = anime.find('div',class_='me-auto no-line-height').find('span',class_='badge score rounded-0').text # rating of the anime
    # year = anime.find('div',class_='animeinfo_top h-100').find('span',class_='badge year rounded-0').text # year of release 
    link = anime.find('a').get('href')
   # raw_data.append([animename,alt,str(year).replace(" ",""),str(rating).replace(" ","")])
    # name.append(animename)
    # rate_list.append(rating)
    links.append(link)



# Rating of the first 10 animes on animedao.to (Bar chart)

first_ten_animes = name[0:10]
first_ten_rates = [eval(i) for i in rate_list[0:10]]

x = np.arange(len(first_ten_animes))
width = 0.35
fig, ax = plot.subplots()
rects = ax.bar(x-width/3,first_ten_rates,label='Rating')
ax.set_ylabel('Rating')
ax.set_title('Rating of the first ten anime on animedao.to')
ax.set_xticks(x,first_ten_animes)
ax.set_xticklabels(first_ten_animes,fontsize=10,rotation=45)
ax.bar_label(rects,padding=3)
fig.tight_layout()
plot.show()





for i in range(len(links[1:18])):
    url  = f"https://animedao.to{links[i]}"
    r = requests.get(url)
    soup = bs(r.text,'html.parser')
    genres = soup.findAll('table',class_='table table-sm')
    for genre in genres:
        types_of_genre = genre.find_all('span',class_='badge badge-genre')
        for t in types_of_genre:
            genres_list.append(t.text)
    

print(genres_list)



'''
Code snippet that parses genre of an anime.

genres = []

URL_test = "https://animedao.to/anime/onepiece"
r = requests.get(URL_test)
soup = bs(r.text,'html.parser')
types_of_genres = soup.findAll('table',class_='table table-sm')
for genre in types_of_genres:
    res = genre.find_all('span',class_='badge badge-genre')
    for r in res:
        genres.append(r.text)


print(genres)

'''
