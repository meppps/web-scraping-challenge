# Dependencies
import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
import json
from splinter import Browser
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

executable_path = {'executable_path':'/usr/local/bin/chromedriver'}

# -- Scrape Function -- #
def scrape():


    # -- ARTICLES -- #

    # Scrape Nasa News Page
    url = 'https://mars.nasa.gov/news/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')

    # Most recent article title
    newsTitle = soup.find('div',class_='content_title').a.text.split('\n')[1]
    print(newsTitle)


    # !!!! NEEDS PARAGRAPH !!!! #


    # -- FEATURED IMAGE -- #
    browser = Browser('chrome', **executable_path, headless=False)


    # Get featured nasa image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)

    # 'view full image'
    browser.find_by_css('.fancybox').click()
    time.sleep(2)


    # more info button
    browser.find_by_css('.button')[2].click()
    time.sleep(1)

    # Full Image (actually)
    featuredImage = browser.find_by_css('.main_image')['src']
    print(featuredImage)
    time.sleep(1)



    # -- MARS WEATHER -- #
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # get first tweet
    weather = browser.find_by_tag('article').value

    # clean up the string
    weather = weather.replace('\n','').split('·')[1]
    print(weather)

    time.sleep(1)


    # -- MARS FACTS -- #
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Get tables from the site
    tables = pd.read_html(url)

    for t in tables:
        print(t,'\n\n\n')

    # df
    marsFacts = tables[0]
    marsFacts

    table = marsFacts.to_html()
    table = table.replace('\n','')
    print(table)

    time.sleep(1)

    # -- HEMISPHERES -- #
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)

    # Loop through for hemisphere links
    hemList = []
    thumbs = browser.find_by_css('.thumb')
    for t in range(len(thumbs)):
        
        browser.find_by_css('.thumb')[t].click()
        time.sleep(1)
        name = browser.find_by_css('.title').value.replace('Enhanced','')
        link = browser.find_by_text('Sample')['href']
        browser.visit(link)
        time.sleep(2)
        imgURL = browser.find_by_tag('img')['src']
        
        # make dictionary, append to list
        hd = {'title':name,'img_url':imgURL}
        hemList.append(hd)
        print(hd)
        
        browser.visit(url)
        time.sleep(1)


    # Return all as dictionary
    # spaceData = {
    #     'news_title':newsTitle,
    #     'featured_image':featuredImage,
    #     'weather':weather,
    #     'marsFacts':marsFacts,
    #     'hems':hemList
    # }

    spaceData = {}
    spaceData['news_title'] = newsTitle
    spaceData['featured_image'] = featuredImage
    spaceData['weather'] = weather
    spaceData['marsFacts'] = table
    spaceData['hemispheres'] = hemList

    return spaceData

    # return {
    #     'news_title':newsTitle,
    #     'featured_image':featuredImage,
    #     'weather':weather,
    #     'marsFacts':marsFacts,
    #     'hems':hemList
    # }

    # print(spaceData)

    # return spaceData


# def scrape():
#     spaceData = {}
#     spaceData['headline'] = 'an interesting title'
#     spaceData['img'] = 'an interesting image'

#     return spaceData

