#!/usr/bin/python
# coding: utf-8
# encoding=utf8
import sys
import datetime
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import os
from parsel import Selector
import urllib.parse
from selenium.common.exceptions import NoSuchElementException
import json
from selenium.webdriver.chrome.options import Options
import shutil
import requests
from osint_sources.recognition import *

def facebook (name_to_search,knownimage):
    print(name_to_search)
    now = datetime.datetime.now()
    os.mkdir( "images/"+str(now) );
    path=os.path.join('images/'+str(now),'facebook_data.json')
    chrome_options = Options()
    jsonData=[]
    chrome_options.add_argument("--headless")

    chrome_path = './chromedriver'
    driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)

    driver.get("https://es-la.facebook.com/public/"+name_to_search)
    driver.implicitly_wait(20)
    
    isMoreButton=True
    while isMoreButton:
        for i in range(1,10):
            isEnd=driver.find_elements_by_id('browse_end_of_results_footer')
            if len(isEnd)>0:
                isMoreButton=False
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
    links=[]
    print('*****Profiles Found*****')
    results=driver.find_elements_by_id('BrowseResultsContainer')[0]
    info=results.find_elements_by_tag_name('a')

    for user in info:
        user_class=user.get_attribute('class')
        if user_class=='_32mo':
            links.append(user.get_attribute('href'))
            print(user.get_attribute('href'))
            user={'name':user.get_attribute('title'),'profile':user.get_attribute('href')}
            jsonData.append(user)

    isMoreButton=True
    i=0
    id_value="fbBrowseScrollingPagerContainer"
    while isMoreButton:
        more=driver.find_elements_by_id(id_value+str(i))
        i=i+1
        if len(more)==0:
            isMoreButton=False
        else:
            div = more[0]
            info=div.find_elements_by_tag_name('a')
            for user in info:
                user_class=user.get_attribute('class')
                if user_class=='_32mo':
                    links.append(user.get_attribute('href'))
                    print(user.get_attribute('href'))
                    user={'name':user.get_attribute('title'),'profile':user.get_attribute('href')}
                    jsonData.append(user)

    now = datetime.datetime.now()
    os.mkdir( "images/"+str(now) );
    path=os.path.join('images/'+str(now),'facebook_data.json')
    with open(path, 'w+') as outfile:
        json.dump(jsonData, outfile)

    j=0
    for l in links:
        driver.get(l)
        div=driver.find_elements_by_class_name('profilePicThumb')[0]
        img=div.find_elements_by_tag_name('img')[0]
        url=img.get_attribute('src')
        name=os.path.join('images/'+str(now),str(j)+"-"+name_to_search+".jpg")
        j=j+1
        try:
            urllib.request.urlretrieve(url, name)
        except:
            pass
    driver.quit()

    if knownimage:
        #face_identification(knownimage,'./images/'+str(now)+'/')
        openface_identification(knownimage,'./images/'+str(now)+'/')
   