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
    file_name = "war1"
    GlobalFunctions.createFile(file_name)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument("headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    path = GlobalVariable.ChromeDriverPath

    scrappedUrl = "https://warsawexpo.eu/en/exhibition-calendar"
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)

    driver.get(scrappedUrl)

    links_raw = driver.find_elements(By.XPATH, "//div[@class='single-callendar-event']//a")

    link_list = []
    for a in links_raw:
        link_list.append(a.get_attribute("href"))
        
#event links
    for link in link_list:
        driver.get(link)
        try:
            s_d_raw = driver.find_element(By.XPATH, "//span[@itemprop='startDate']")
            e_d_raw = driver.find_element(By.XPATH, "//span[@itemprop='endDate']")
            if True:
                try:
                    s_d_split = s_d_raw.text.split("-")
                    e_d_split = e_d_raw.text.split("-")

                    s_y, e_y = s_d_split[-1], e_d_split[-1]
                    s_m, e_m = s_d_split[1], e_d_split[1]
                    s_d, e_d = s_d_split[0], e_d_split[0]
#dates
                    startDate = f"{s_y}-{s_m}-{s_d}"
                    endDate = f"{e_y}-{e_m}-{e_d}"
                except:
                    s_d_split = " "
                    e_d_split = " "
#event name
                try:
                    event_name = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text
                except:
                    event_name = " "
#orgName
                try:
                    orgName = driver.find_element(By.XPATH, "//h5[@class='organizer']").text.title()
                except:
                    orgName = " "
#orgWeb                    
                try:
                    orgWeb_raw= driver.find_elements(By.XPATH, "//div[@class='uncont']//div[@class='uncode_text_column ']//p//a")
                    if len(orgWeb_raw)>2:
                        orgWeb = orgWeb_raw[2].text
                    else:
                        orgWeb = "https://warsawexpo.eu/"
                except:
                    orgWeb_raw = " "
#contact 
                try:
                    contact = driver.find_element(By.XPATH, "//div[@class='uncont']//div[@class='uncode_text_column ']//p//a[1]").text
                except:
                    contact = " "
#contactEmail
                try:
                    cmail = driver.find_element(By.XPATH, "//div[@class='uncont']//div[@class='uncode_text_column ']//p//a[2]").text
                except:
                    cmail = " "
#city & country & venue
                try:
                    venue = driver.find_element(By.XPATH, "//div[@class='uncode_text_column']//span[@itemProp='name']").text + "-" + driver.find_element(By.XPATH, "//span[@itemProp='address']").text.replace("\n", " ")
                    city = driver.find_element(By.XPATH,"//div[@class= 'uncode_text_column']//span[@itemprop='addressRegion']").text
                    country = driver.find_element(By.XPATH,"//div[@class= 'uncode_text_column']//span[@itemprop='address']").text.split("\n")[-1].split(",")[-1].strip()

                    formated_venue = re.sub(r"[(0-9)]", "",venue).replace("  ", "")

                    if formated_venue:
                        emode = 0
                    else:
                        emode = 1
                except:
                    venue = " "
                    city = " "
                    country = " "
#google location
                try:
                    google_location = GlobalFunctions.get_google_map_url(venue.split("-")[0], driver)
                except:
                    google_location = ''
            else:
                continue
        except:
            continue

        GlobalFunctions.appendRow(file_name,[scrappedUrl, event_name, startDate, endDate, '', '', '', '', orgName,
                                           orgWeb, '', '', '', '', '', city, country, formated_venue, link,
                                           google_location, cmail, '', emode])



except Exception as e:
    print(e)
    error = str(e)
# except:
#     pass
    
GlobalFunctions.update_scrpping_execution_status(file_name, error)
driver.quit()