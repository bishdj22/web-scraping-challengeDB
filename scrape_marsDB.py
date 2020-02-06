#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import lxml.html as lh

# Activate PRIOR TO SUBMISSION:

import warnings
warnings.filterwarnings("ignore")

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_test():
    #Scrape NASA headlines
    mars_data = {}

    browser = init_browser()

    # Visit mars.nasa.gov
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape latest news title and corresponding paragraph

    news_title = soup.find("div", class_="content_title").get_text()
    news_p = soup.find("div", class_="article_teaser_body").get_text()

    # Dictionary of results
    marsnews_data = {
        "News": news_title,"Teaser": news_p}

    # Close the browser after scraping
    browser.quit()
    
    #---1. Add Mars News to Function Dictionary---> marsnews_data

    #Scrape for featured image + URL
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    browser.click_link_by_id('full_image')
    browser.click_link_by_partial_href('/spaceimages/details.php')       

    img_path = "https://photojournal.jpl.nasa.gov/jpeg/"
    scrape_pic = browser.links.find_by_partial_text('.jpg')


    feat_path = scrape_pic.text

    feat_img_url = (img_path+feat_path)

    browser.quit()
    
    #---2. Add Mars Featured Image URL to Function Dictionary---> feat_img_url


    #MARS facts URL

    facts_url = "https://space-facts.com/mars/"


    # Locate HTML table
    tables = pd.read_html(facts_url)
    tables


    # Table to DataFrame

    df = tables[2]
    df.columns = ['0','1']
    mars_df = df.rename(columns={"0": "Title", "1": "Data"})
    mars_df


    # Convert the data to a HTML table string

    html_table = mars_df.to_html()
    
    #---3. Add HTML Facts Table to Function Dictionary---> html_table

    # ----- TWITTER SCRAPING ------#

    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException
    from splinter import Browser


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', executable_path, headless=True)

    #Scrape Weather Tweet

    browser = init_browser()

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    #timeout = 5


    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('div', class_= "css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").get_text()

    browser.quit()

    #---4. Add Twitter Weather to Function Dictionary---> mars_weather

    #-----------------Mars Hemispheres Images----------------------#


    browser = init_browser()
    mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    #Scrape Images & URL
    browser.visit(mars_url)

    mars_hemispheres = browser.html
    soup = bs(mars_hemispheres, 'html.parser')

    images = soup.find_all('div', class_='item')


    base_usgs_url = "https://astrogeology.usgs.gov"
    images_list = []

    for image in images:
        title = image.find('h3').text
        pic_url = image.find('a',class_="itemLink product-item")['href']
        browser.visit(base_usgs_url + pic_url)
        pic = browser.html
        soup = bs(pic, 'html.parser')
        img_url = base_usgs_url + soup.find('img', class_='wide-image')['src']
        images_list.append({"title" : title, "img_url" : img_url})
        
    browser.quit()
    
    #Store data & links in Dictionary#
    mars_data = {"mars_news": marsnews_data, "featured_image":feat_img_url, 
        "html_table":html_table, "weather":mars_weather, 
        "image_list":images_list
    }

    return mars_data

    #Why does return not return anything? but runs through function




