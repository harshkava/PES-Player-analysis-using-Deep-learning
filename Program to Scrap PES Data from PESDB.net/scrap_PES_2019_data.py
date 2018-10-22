# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 17:52:30 2018

@author: Harsh Kava
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv
import time


#make browser

ua = UserAgent()
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (ua.random)
service_args=['--ssl-protocol=any','--ignore-ssl-errors=true']
driver = webdriver.Chrome('chromedriver.exe',desired_capabilities=dcap,service_args=service_args)

webLink = 'http://pesdb.net/pes2019/'
data = []

for i in range(1,350):
        
    try:
        driver.get(webLink+'?page='+str(i))    #visiting each page  #Page format = http://pesdb.net/pes2019/?page=349
        html=driver.page_source # get the html
        soup = BeautifulSoup(html, "lxml") # parse the html 
        
        table = soup.find('table', attrs={'class':'players'})#get the table
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
    
        for row in rows:
            cols = row.find_all('td')
            cols = [values.text.strip() for values in cols]
            data.append(cols)
            
        # Wait for 5 second
        time.sleep(5)
        #print(data)
    except Exception as e:
        print ( 'Error in parsing data :: ', e)
           

#creating a new csv file from data
with open('PES2019.csv', 'w', newline='',encoding='utf8') as myfile:
     wr = csv.writer(myfile)
     header=['Position',	'Player Name',	'Team Name',	'Nationality',	'Height', 	'Weight' 	,'Age', 	'Condition' 	,'Overall Rating']
     try:
         wr.writerow(header)
         for row in data:
             wr.writerow(row)
     except Exception as e:
        print('Error in writing data to csv :: ',e)
    