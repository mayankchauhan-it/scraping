from bs4 import BeautifulSoup
from selenium import webdriver
import csv


def getting_url(search_name):
    base_url = "https://www.amazon.in/s?k={}"
    search_name = search_name.replace(' ', '+')
    new_url = base_url.format(search_name)
    new_url += "&page={}"
    return new_url


def scrap_data(item):
    # PRODUCT NAME AND URL:
    product_name = item.h2.a.text
    product_url = ('https://www.amazon.in/' + item.h2.a.get('href'))

    try:
        # price
        product_price = item.find('span', 'a-price-whole').text
    except AttributeError:
        return

    try:
        # rating & Number of Reviews
        product_rating = item.i.text

        num_of_review = item.find('span', {'class': 'a-size-base'}).text
    except AttributeError:
        product_rating = ' '
        num_of_review = ' '

    asin = [item['data-asin']]  # ASIN Details

    results1 = (product_name, product_price, product_rating, num_of_review, product_url, asin)
    return results1


def scrap_data2(item):
    Description = item.find('span', {'id': 'productTitle'}).text

    try:
        product_description = item.find('div', {'id': 'productDescription'}).getText()
    except:
        product_description = "Not Available"

    results1 = (Description, product_description)
    return results1


def scrap(search_name):
    driver = webdriver.Chrome()
    url = getting_url(search_name)

    record = []
    record2 = []

#fatching details.

    for page in range(1,20):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        result = soup.find_all('div', attrs={"data-component-type": "s-search-result"})

        for item in result:
            records = scrap_data(item)

            if records:
                record.append(records)
        driver.get(url.format(page))


#Here To execute both part, I have used two for loop for two difference task.
#Hiting each url :

    for page in range (1,20):
        driver.get(url.format(page))
        soup2 = BeautifulSoup(driver.page_source, "html.parser")
        result2 = soup2.find_all('div', attrs={"data-component-type": "s-search-result"})

        link2 = []

        for item in result2:
            product_url = ('https://www.amazon.in/' + item.h2.a.get('href'))
            link2 += product_url

#instead of targeting list of url, Here I have preferred to target each link one by one. While Calling from list, I found link is not in squence as search list. So I have preferred to call each link one by one.

            driver.get(product_url)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            result2 = soup.find_all('div', {'id': 'dp-container'})

            for item in result2:
                second_part = scrap_data2(item)

                if second_part:
                    record2 += second_part

        driver.get(url.format(page))


        # for item in link:
        #     driver.get(item)
        #     soup = BeautifulSoup(driver.page_source, "html.parser")
        #     result2 = soup.find_all('div', {'id': 'dp-container'})
        #
        #     for item in result2:
        #         second_part = scrap_data2(item)
        #
        #         if second_part:
        #             record2.append(second_part)

        # driver.get(url.format(page))  # head back to search page.

    driver.close()

    with open('Final data.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Product_Name', 'Price', 'Rating', 'Review Count', 'URL', 'ASIN'])
        writer.writerows(record)



scrap('bags')
