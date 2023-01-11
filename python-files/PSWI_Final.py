# Created by : Mayank Chauhan
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys
import json
from random import randint
import time
import requests
from datetime import datetime
import re

sys.path.insert(0, os.path.dirname(__file__).replace('python-files','global-files/'))
from GlobalVariable import *
from GlobalFunctions import *



try:
    file_name="pswi"

    GlobalFunctions.createFile(file_name)   #to created TSV file with header line

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    path = GlobalVariable.ChromeDriverPath
    driver = webdriver.Chrome(options=options, executable_path=path)

    error = ''

#Scrapped Url
    scraped_url = 'https://www.pswi.org/Education/Conferences'

    driver.get(scraped_url)
    driver.minimize_window()


    raw = driver.find_elements(By.XPATH, "//div[@class='row Pane']//p")

    
    for i in raw:

#orgName & orgWeb:
        orgName = driver.find_element(By.XPATH, "//a[@id='dnn_dnnLogoXS_hypLogo']").get_attribute("title")
        orgWeb = driver.find_element(By.XPATH, "//a[@id='dnn_dnnLogoXS_hypLogo']").get_attribute("href")

        raw_split = i.text.splitlines()


        if len(raw_split)>2 and len(raw_split)<4:

            new_raw_split = raw_split

#event links:
            try:
                event_link = i.find_element(By.TAG_NAME,"a").get_attribute("href")

            except:
                event_link = ' '

#Date & Time
            try:
                date_raw = new_raw_split[1].split(",")

                if len(date_raw)>1:
                    year, month = date_raw[-1].strip(), date_raw[-2].strip().split(" ")[0]

                    try:
                        event_name = new_raw_split[0]
                    except:
                        event_name = " "

                    try:
                        s_d, e_d = date_raw[-2].strip().split(" ")[1].split("-")[0].zfill(2), date_raw[-2].strip().split(" ")[1].split("-")[1].zfill(2)
                        startDate, endDate = f"{year}-{GlobalVariable.months[month]}-{s_d}", f"{year}-{GlobalVariable.months[month]}-{e_d}"
                    
                    except:
                        s_d = date_raw[-2].strip().split(" ")[1].split("-")[0].zfill(2)
                        e_d = s_d

                        startDate, endDate = f"{year}-{GlobalVariable.months[month]}-{s_d}", f"{year}-{GlobalVariable.months[month]}-{e_d}"
                    
#venue
                    try:
                        venue_raw = raw_split[2].split(",") 

                        try:
                            venue = venue_raw[0]

                            
                        except:
                            venue = "Blank"
                        
                        if venue:
                                emode = 0
                        else:
                            emode = 1

#City & Country
                        try:
                            city = venue_raw[1].strip()

                            try:
                                country = venue_raw[2].strip()

                            except:
                                country = ' '


                        except:
                            city = ' '
                            country =  ' '

                    except:
                        pass

#contact information            
                    try:
                        cmail = driver.find_element(By.XPATH, "//ul[@class='psw-site-info']/li[1]/a").text
                    except:
                        cmail = "info@pswi.org"


                else:
                    continue

            except:
                date_raw = ' '
                pass


        else:
            continue
        
        GlobalFunctions.appendRow(file_name, [scraped_url, event_name, startDate, endDate, '', '', '', '', orgName,
                                            orgWeb, '', '', '', '', '', city, country, venue, '',
                                            " ", cmail, '', emode])



except Exception as e:
    print(e)
    error = str(e)


GlobalFunctions.update_scrpping_execution_status(file_name, error)
driver.quit()