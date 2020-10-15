#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# In[22]:


#Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo




#link to chromedriver
def init_browser():
 executable_path = {'executable_path': '/Users/asna_/Desktop/chromedriver.exe'}
 return Browser('chrome', **executable_path, headless=False)


# ### NASA Mars News

# In[24]:


#URL of the NASA page which is scraped
def scrape():
    browser=init_browser()
    mars_data={}
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(5)

    # In[4]:


    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


  


    #Examine the results and determine elements that contains sought info 
    #print(soup.prettify())


    # In[26]:


    # Extracts the latest News Title - # does not run in vs code
    step1=soup.select_one("ul.item_list li.slide")
    news_title = step1.find('div',class_='content_title').text
    news_title


    # In[27]:


    #extracting the paragraph text of latest News Article
    News_p=step1.find('div',class_='article_teaser_body').text
    News_p


    # ### JPL Mars Space Images - Featured Image

    # In[8]:


    # Use Splinter to navigate the following site and find the image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(2)

    # In[9]:


    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)


    # In[10]:


    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')


    # In[11]:


    step1=soup.select_one("figure.lede a img").get("src")
    step1


    # In[12]:


    featured_image_url="https://www.jpl.nasa.gov"+step1
    featured_image_url


    # ### Mars Facts

    # In[13]:


    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)


    # In[14]:


    # Use Pandas to scrape the table containing facts about the planet including diameter, mass, etc
    fact_table = pd.read_html(facts_url)
    df = fact_table[2]
    df.columns = ['Mars Facts','Value']
    df.set_index(['Mars Facts'], inplace = True)
    df.to_html('Mars_df.html')
    df


    # In[15]:


    # Use Pandas to convert the data to a HTML table string.
    mars_fact = df.to_html(classes='table table-striped')


    # In[16]:


    mars_fact


    # ### Mars Hemispheres

    # In[17]:


    image_url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(image_url)


    # In[18]:


    time.sleep(2)


    # In[19]:


    #reading h3 tag 
    links= browser.find_by_css("a.product-item h3")


    # In[20]:


    #create an empty listfirst 
    hemidic= []

    for i in range(len(links)):
        hemi = {}
        
        browser.find_by_css('a.product-item h3')[i].click()
        hemi['img_url'] = browser.find_by_text('Sample')['href']
        hemi['title'] = browser.find_by_css('h2.title').text
        
        hemidic.append(hemi)
        browser.back()

    mars_info={
        "news_title":news_title,
        "news_p":News_p,
        "featured_image_url":featured_image_url,
        "mars_fact":str(mars_fact),
        "hemidic":hemidic
    }
    browser.quit()
    return mars_info

# In[ ]:




