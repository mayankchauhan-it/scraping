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

    file_name = "iarai"
    GlobalFunctions.createFile(file_name)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument("headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    path = GlobalVariable.ChromeDriverPath

    scrappedUrl = "https://www.iaria.org/conferences23.html"
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)

    driver.get(scrappedUrl)

    error = ' '
    raw = driver.find_elements(By.XPATH, "//div[@class='second']/ul//li//a")
    cmail = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/a").get_attribute("href").split(":")[1]

    event_link_list = []
    for i in raw:
        event_link = i.get_attribute("href")
        # event_name = i.text

        event_link_list.append(event_link)

#event link
    for k in range(len(event_link_list)):
        driver.get(event_link_list[k])

        e_link = event_link_list[k]

        try:
            raw2 = driver.find_element(By.CLASS_NAME, "conflabels").text.split("\n")[-1].split(" - ")
#event name
            try:
                event_name = driver.find_element(By.XPATH, "//div[@class='conflabels']/h2[1]").text
            except:
                event_name = ' '
#city & country
            try:
                city = raw2[-1].split(",")[-2].strip()
                country = raw2[-1].split(",")[-1].strip()

            except:
                city = " "
                country = " "

            if country:
                emode = 0
            else:
                emode= 1
#Date of the event
            try:
                date_raw = raw2[0].split(" to ")
                start_date_raw, end_date_raw = date_raw[0].split(","), date_raw[1].split(",")
                year = start_date_raw[-1].strip() # 2023
                s_m,e_m  = start_date_raw[0].split(" ")[0], end_date_raw[0].split(" ")[0]
                starting_month, ending_month = GlobalVariable.months[s_m], GlobalVariable.months[e_m] #converting month with variable
                s_d, e_d = start_date_raw[0].split(" ")[1], end_date_raw[0].split(" ")[1]

                startdate = f"{year}-{starting_month}-{s_d}"
                enddate = f"{year}-{ending_month}-{e_d}"

            except Exception as e:
                startdate = " "
                enddate = " "
                print(e)
#venue
            try:
                btn = driver.find_element(By.XPATH,"//div[@class='menudiv']//div[@class='dropdown'][2]//a[2]").get_attribute("href")
                driver.get(btn)

                venue = driver.find_element(By.XPATH, "//p[@align='left'][2]//strong").text.title()

                # if venue:
                #     try:
                #         google_location = GlobalFunctions.get_google_map_url(venue, driver)
                #     except:
                #         google_location = ''
                # else:
                #     continue

            except Exception as e:
                print(e)

        except:
            continue

        orgName = "IARIA"
        orgWeb = "https://www.iaria.org/"

        GlobalFunctions.appendRow(file_name, [scrappedUrl, event_name, startdate, enddate, '', '', '', '', orgName,
                                          orgWeb, '', '', '', '', '', city, country, venue, e_link,
                                          """google_location""", cmail, '', emode])
except Exception as e:
    pass


GlobalFunctions.update_scrpping_execution_status(file_name, error)
driver.quit()