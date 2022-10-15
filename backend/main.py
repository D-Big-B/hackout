from bs4 import BeautifulSoup
import fastapi
import requests
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = FastAPI()


@app.get('/')
def get_root():
    return {"data": "hey api is working 😊😊😊😊"}


@app.get("/api/v1/city")
def get_city():
    city_html_text = requests.get(
        'https://www.headout.com/').text
    city_soup = BeautifulSoup(city_html_text, 'lxml')
    city_lateral_carousel = city_soup.find(
        'div', class_='lateralCarousel__InnerCarouselWrapper-sc-5y1ry2-1 kuxOjf')
    city_card_datas = city_lateral_carousel.find_all(
        'a', class_='city-card-link-wrapper')
    city_data = []
    for card_data in city_card_datas:

        city_data.append(
            {
                "cityImage": card_data.find(
                    "div", class_='city-image-wrapper').span.noscript.img['src'],
                "cityTitle": card_data.find(
                    "div", class_="city-bottom-wrapper").find('div', class_='city-title').text,
                "cityTagLine": card_data.find(
                    "div", class_="city-bottom-wrapper").find('div', class_='city-tag-line').text,
                "cityLink": card_data['href']})
    return city_data


@app.get('/api/v1/product/{product_link}')
def get_product(product_link: str):
    product_html_text = requests.get(
        f'https://www.headout.com/{product_link}').text
    product_soup = BeautifulSoup(product_html_text, 'lxml')
    product_lateral_carousel = product_soup.find(
        'div', class_='lateralCarousel__InnerCarouselWrapper-sc-5y1ry2-1')
    product_card_datas = product_lateral_carousel.find_all(
        'div', class_='product-card-v2')
    product_data = []
    for card_data in product_card_datas:

        product_data.append(
            {
                "productImage": card_data.div.span.noscript.img["src"],
                "productBooster": card_data.find(
                    "div", class_="productCardComponent__ProductContent-sc-hogtmy-3").find('div', class_='productCardComponent__L2Booster-sc-hogtmy-4').span.text,
                "productTitle": card_data.find(
                    "div", class_="productCardComponent__ProductContent-sc-hogtmy-3").a.text,
                "productLink": card_data.find(
                    "div", class_="productCardComponent__ProductContent-sc-hogtmy-3").a['href']
            })
    return product_data


@app.get('/api/v1/productOverview/{product_link}/{productOverview_link}')
def getProductOverview(product_link: str, productOverview_link: str):
    productOverview_html_text = requests.get(
        f'https://www.headout.com/{product_link}/{productOverview_link}').text
    productOverview_soup = BeautifulSoup(productOverview_html_text, 'lxml')

    productOverview_data = {
        "productOverviewHeading": productOverview_soup.find(
            'div', class_="productOverview__ProductNameWrapper-sc-nd2ro4-1").h1.text,
        "productOverviewContent": productOverview_soup.find(
            'div', class_="content-html").p.text,
        "productOverviewHighlights": str(productOverview_soup.find("div", class_="accordionContentSection__HtmlContentWrapper-sc-ovha8c-2").div.ul)
    }
    return productOverview_data


@app.get('/api/v1/productPrice/{product_booster}')
def getProductPrice(product_booster: str):
    product_price = []

    # Headout Price
    headout_url = f'https://www.headout.com/search/?q={product_booster}'
    headout_driver = webdriver.Chrome(
        executable_path="C:\webdriver\chromedriver.exe")
    headout_driver.get(headout_url)
    product = headout_driver.find_element(By.CLASS_NAME, 'product-card')
    headout_price = product.find_element(
        By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/span').text
    if headout_price == 'from':
        headout_price = product.find_element(
            By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[2]').text
    print('headout price : ', headout_price)
    product_price.append({"headout_price": headout_price})

    # Viator Price
    viator_url = f'https://www.viator.com/searchResults/all?text={product_booster}'
    viator_driver = webdriver.Chrome(
        executable_path="C:\webdriver\chromedriver.exe")

    viator_driver.get(viator_url)

    viator_price = viator_driver.find_element(
        By.XPATH, '/html/body/div[2]/div[7]/div/div[1]/div[2]/div[2]/div[3]/div/div[3]/div/div[1]/div/div/div/div[3]/div/div/div/div[2]').text
    product_price.append({"viator_price": viator_price})

    # Thrillophilla Price
    thrillophilla_url = f'https://www.thrillophilia.com/listings/search?search={product_booster}'

    thrillophilla_driver = webdriver.Chrome(
        executable_path="C:\webdriver\chromedriver.exe")

    thrillophilla_driver.get(thrillophilla_url)

    thrillophilla_price = thrillophilla_driver.find_element(
        By.XPATH, '/html/body/div/div/main/div[3]/div/form/div[3]/div[2]/div[2]/span[2]/div[3]/div/div[3]/div/p/span[1]').text
    product_price.append({"thrillophilla_price": thrillophilla_price})

    # Tiquet Price
    tiquet_url = f'https://www.tiqets.com/en/search?q={product_booster}s'
    tiquet_driver = webdriver.Chrome(
        executable_path="C:\webdriver\chromedriver.exe")
    tiquet_driver.get(tiquet_url)
    delay = 5
    myElem = WebDriverWait(tiquet_driver, delay).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/div[2]/div/div[2]/article[1]/div[2]/footer/div/div[2]/span[2]')))

    print('Tiquet price : ', myElem.text)
    product_price.append({'tiquet_price': myElem.text})

    return (product_price)
