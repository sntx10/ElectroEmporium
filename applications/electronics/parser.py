import time

import requests
from bs4 import BeautifulSoup as Bs
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

ua = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={ua.chrome}')
options.add_argument('--headless')
options.add_argument('--disable-blink-features=AutomationControlled')


class PlanetaParser:
    def __init__(self, url):
        self.url = url

    def _get_html(self):
        return requests.get(self.url).text

    def _get_soup(self):
        html = self._get_html()
        return Bs(html, 'lxml')

    @staticmethod
    def _validate_price(price: str) -> int:
        """
        превращает в цену в тип данных int
        :param price: цена
        """
        res = ''
        for letter in price:
            if letter.isdigit():
                res += letter
        return int(res)

    def get_data(self):
        soup = self._get_soup()
        catalog = soup.find('div', class_='catalog__goods').find('div', class_='goods__wrapper')
        products = catalog.find_all('section', class_='product__card')
        data = []
        for product in products[:3]:
            try:
                title = product.find('span', class_='visually-hidden').text.strip()
            except AttributeError:
                title = ''
            try:
                price = product.find('div', class_='card__price').text.strip()
                price = self._validate_price(price)
            except AttributeError:
                price = 0
            try:
                img_links = product.find('a', class_='card__image-box').find_all('img', 'card__image')
                images = []
                for image in img_links:
                    images.append(image.get('src'))
            except AttributeError:
                images = []
            data.append(
                {
                    'title': title,
                    'images': images,
                    'price': price
                }
            )
        return data


class SoftechParser(PlanetaParser):
    def _get_html(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(self.url)
        time.sleep(2)
        return driver.page_source

    def get_data(self):
        soup = self._get_soup()
        catalog = soup.find('div', class_='tab-content')
        products = catalog.find_all('div', class_='product-layout')
        data = []
        for product in products:
            try:
                title = product.find('div', class_='right').h2
                title = title.text.split(' ')
                title = ' '.join([i.replace('\n', '') for i in title if i])
            except AttributeError:
                title = ''
            try:
                price = product.find('span', class_='price-new').text
                price = self._validate_price(price)
            except AttributeError:
                price = 0
            try:
                images = []
                image_links = product.find('a', class_='lazy').find_all('img', class_='img-responsive')
                for image in image_links:
                    images.append(image.get('data-src'))
            except AttributeError:
                images = []
            data.append({
                'title': title,
                'images': images,
                'price': price
            })
        return data


class SystemaParser(SoftechParser):
    def get_data(self):
        soup = self._get_soup()
        catalog = soup.find('div', class_='products')
        products = catalog.find_all('div', class_='product')
        data = []
        for product in products[:3]:
            try:
                images = [product.find('a', class_='thumbnail').img.get('data-full-size-image-url')]
            except AttributeError:
                images = []
            try:
                title = product.find('div', class_='product-description').h3.text.split()
                title = ' '.join(i for i in title if i)
            except AttributeError:
                title = ''
            try:
                price = product.find('span', class_='price').text.strip()
                price = self._validate_price(price)
            except AttributeError:
                price = 0
            data.append({
                'title': title,
                'images': images,
                'price': price
            })
        return data


def get_recommend_data():
    """
    возвращает все полученные с трех сайтов данные об актуальных товарах
    :return:
    """
    planeta = PlanetaParser(
        'https://planeta.kg/catalog?cat_id=&sorter=count_buy%7C1&price_course%5B%5D=0&price_course%5B%5D=649990&applyFilter=1')
    softech = SoftechParser(
        'https://softech.kg/'
    )
    systema = SystemaParser(
        'https://systema.kg/'
    )
    data = []
    site_list = [planeta, softech, systema]
    for i in site_list:
        data.extend(i.get_data())
    return data
