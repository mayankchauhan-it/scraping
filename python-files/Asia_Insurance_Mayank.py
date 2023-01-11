from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import os
from datetime import date, time
import re
from re import *

sys.path.insert(0, os.path.dirname(__file__).replace('parsing-new-script', 'global-files/'))
# from GlobalVariable import *
from GlobalFunctions import *

try:
    file_name = "AsianInsurance"

    GlobalFunctions.createFile(file_name)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('window-size=800x600')

    path = GlobalVariable.ChromeDriverPath
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)

    scrappedUrl = "https://www.asiainsurancereview.com/Conferences" #scrapped URL Defined

    driver.get(scrappedUrl)
    
    links_f = []
    # try:
    links = driver.find_elements(By.XPATH, "//*[@id='dnn_ctr28907_ViewAllConference_main_div']/div/div[3]/div/div/div[1]/h4/a")
    # print(links)

    for i in links:
        link_list = i.get_attribute("href")
        links_f.append(link_list)
    
    
    
    for i in links_f:
        event_website = i
        orgWeb = scrappedUrl.split("/")[-2]
        orgName = " Asia Insurance Review "

        driver.get(i)  
        
        
        try:
            ename = driver.find_element(By.XPATH, "//h1[@id='dnn_ctr29234_ViewPreConfHeader_h1_confTitle']").text
            print(f"Event Name : {ename}")
            
            date_name_raw = driver.find_element(By.XPATH, "//h2[@id='dnn_ctr29234_ViewPreConfHeader_div_confDatePlace']").text

            date_raw_splited = date_name_raw.split(",") #['27-28 Sep 2023', ' Kuala Lumpur', ' Malaysia'] ['11-12 Oct 2023', ' Singapore']

            splite_target = date_raw_splited[0].split(" ") #['17', 'Nov', '2023'] ['Oct', '2023'] ['11-12', 'Oct', '2023']
            year = splite_target[-1]

            month_raw = splite_target[-2]
            month = GlobalVariable.months[month_raw]
            
            
            if len(date_raw_splited) > 2:
                try:
                    country = date_raw_splited[-1]
                    event_mode = "0"
                except:
                    country = " "
                    event_mode = "1"
                
                try:
                    city = date_raw_splited[-2]
                except:
                    city = " "

            else:
                try:
                    city = ''
                except:
                    city = " "
                try:
                    country = date_raw_splited[-1]
                    event_mode = "0"
                    
                except:
                    country = " "
                    event_mode = "1"
            
            try:
                date_raw_target = splite_target[-3] 
                try:
                    date_raw_target = date_raw_target.split("-")
                    sdate = date_raw_target[0]
                    edate = date_raw_target[1]

                except:
                    sdate = date_raw_target[0]
                    edate = sdate

                startdate = f"{year}-{month}-{sdate}"
                enddate = f"{year}-{month}-{edate}" 
            except:
                continue

        
        
        except:
            
            try:
                ename = driver.find_element(By.XPATH, "//h1[@id='dnn_ctr29316_ViewPreConfHeader_h1_confTitle']").text
                
                
                date_name_raw = driver.find_element(By.XPATH, "//h2[@id='dnn_ctr29316_ViewPreConfHeader_div_confDatePlace']").text

                date_raw_splited = date_name_raw.split(",")

                splite_target = date_raw_splited[0].split(" ") #['17', 'Nov', '2023'] ['Oct', '2023'] ['11-12', 'Oct', '2023']
                year = splite_target[-1]

                month_raw = splite_target[-2]
                month = GlobalVariable.months[month_raw]
                
                
                
                if len(date_raw_splited) > 2:

                    try:
                        country = date_raw_splited[-1]
                        event_mode = "0"
                    except:
                        country = " "
                        event_mode = "1"

                    try:
                        city = date_raw_splited[-2]
                    except:
                        city = " "

                else:
                    try:
                        city=''
                        country = date_raw_splited[-1]
                        event_mode = "0"
                        
                    except:
                        city=''
                        country = " "
                        event_mode = "1"
                
                try:
                    date_raw_target = splite_target[-3]
                    try:
                        date_raw_target = date_raw_target.split("-")
                        sdate = date_raw_target[0]
                        edate = date_raw_target[1]

                    except:
                        sdate = date_raw_target[0]
                        edate = sdate

                    startdate = f"{year}-{month}-{sdate}"
                    enddate = f"{year}-{month}-{edate}" 
                except:
                    continue

            except:
                continue


        GlobalFunctions.appendRow(file_name,[scrappedUrl, ename, startdate, enddate, '', '', '', '', orgName,
                                    orgWeb, '', '', '', '', '', city, country, '', event_website,
                                    '', '', '', event_mode])

except Exception as e:
    print(e)
    error = str(e)

GlobalFunctions.update_scrpping_execution_status(file_name, error)
# driver.quit()