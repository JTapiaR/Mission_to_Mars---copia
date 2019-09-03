import requests
from pathlib import Path
import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import html
import twitter
import tweepy 
from tweepy.auth import OAuthHandler
from lxml import html
from twython import Twython, TwythonError
import config

def init_driver():
    executable_path ="C:\\Users\\JESICA\\Anaconda3.5\\envs\\gdal_env\\Lib\\site-packages\\selenium\\webdriver\\firefox"
    driver = webdriver.Firefox(executable_path)
    return driver

def scrape():
    driver = init_driver()
    news_title,news_p=news_mars()

    infomars={
        "newstitle":news_title,
        "newsbody":news_p,
        "MarsImage":Featured_Image(),
        "weather":Mars_Weather(),
        "facts":Mars_Facts(),
        "hemispheres":Mars_Hemispheres(),
    }
    driver.close()
    return infomars

#NEWS MARS
def news_mars():
     driver = init_driver()
     url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
     driver.get(url)
     r=requests.get(url)
     soup = BeautifulSoup(r.content)
     news_1p= soup.find('div',class_="article_teaser_body")
     news_title=driver.find_element_by_class_name("content_title").text
     news_p=driver.find_element_by_class_name("article_teaser_body").text                  
     #print(news_title,news_p)
     #news_dict={"newstitle":news_title,"newsbody":news_p}
     driver.close()
     return news_title,news_p

#Featured Image
def Featured_Image():
     driver = init_driver()
     url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
     driver.get(url)
     img = driver.find_element_by_id('full_image').click()
     time.sleep(15)
     img2=driver.find_element_by_xpath('//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]').click()
     featured_image_url=driver.find_element_by_class_name("main_image").get_attribute("src")
     driver.close()
     #print(featured_image_url)
     #image_dict={"MarsImage":featured_image_url}
     return featured_image_url

#Mars Weather
def Mars_Weather():
     driver = init_driver()
     auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
     auth.set_access_token(config.access_token,config.token_secret)
     api = tweepy.API(auth)
     api
     twitter_api = twitter.Twitter(auth=auth)
     searchQuery = api.user_timeline(screen_name='@MarsWxReport')
     tweets = api.user_timeline(screen_name='@MarsWxReport', count=2,include_rts = False,tweet_mode = 'extended')
     for info in tweets[:3]:
        mars_weather=[]
        print(info.full_text)
        Tex=(info.full_text)
        mars_weather.append(Tex)    
        print("\n")
        #marsweather_dict ={"last_tweet":mars_weather}
        driver.close()
        return mars_weather[0]
     
#Mars Facts
def Mars_Facts():
     driver = init_driver()
     url="https://space-facts.com/mars/"
     res = requests.get(url)
     soup = BeautifulSoup(res.text,"html")
     table=[]
     for tr in soup.find(class_="tablepress tablepress-id-p-mars").find_all("tr"):
         data = [item.get_text(strip=True) for item in tr.find_all(["h3","th","td"])]
         table.append(data)
         table
         table.append(data)
         tabledf=pd.DataFrame(table)
         tabledf.rename(columns={tabledf.columns[0]:"Parameter",tabledf.columns[1]:"Value"}, inplace = True)
         tabledf
         #FactsMarsTable=tabledf.to_dict('records')
         FactsMarsTable= tabledf.to_html(header=False, index=False)
         #FactsMarsTable=FactsMarsTable.replace('\n', '')
         #FactsMarsTable=list(table)
         driver.close()
         return FactsMarsTable[0]
         #return tabledf
#Mars Hemispheres
def Mars_Hemispheres():
    driver = init_driver()
    driver=webdriver.Firefox()
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver.get(url)
    hemisdic=[]
    time.sleep(15)
    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/section/div/div[2]/div[1]/div/a/h3").click()
    time.sleep(15)
    featured_image_url=driver.find_element_by_class_name("wide-image").get_attribute("src")
    tit=driver.find_element_by_xpath('//*[@id="splashy"]/div[1]/div[1]/div[3]/section/h2[1]').text
    hemisdic.append({"title" : tit, "img_url" : featured_image_url})
    driver.get(url)
    time.sleep(10)
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/section/div/div[2]/div[2]/div/a/h3').click()
    tit=driver.find_element_by_xpath('//*[@id="splashy"]/div[1]/div[1]/div[3]/section/h2[1]').text
    time.sleep(15)
    featured_image_url=driver.find_element_by_class_name("wide-image").get_attribute("src")
    hemisdic.append({"title" : tit, "img_url" : featured_image_url})
    driver.get(url)
    time.sleep(10)
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/section/div/div[2]/div[3]/div/a/h3').click()
    tit=driver.find_element_by_xpath('//*[@id="splashy"]/div[1]/div[1]/div[3]/section/h2[1]').text
    time.sleep(15)
    featured_image_url=driver.find_element_by_class_name("wide-image").get_attribute("src")
    hemisdic.append({"title" : tit, "img_url" : featured_image_url})
    driver.get(url)
    time.sleep(10)
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/section/div/div[2]/div[4]/div/a/h3').click()
    tit=driver.find_element_by_xpath('//*[@id="splashy"]/div[1]/div[1]/div[3]/section/h2[1]').text
    time.sleep(15)
    featured_image_url=driver.find_element_by_class_name("wide-image").get_attribute("src")
    hemisdic.append({"title" : tit, "img_url" : featured_image_url})
    driver.close()
    return hemisdic
         