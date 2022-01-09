'''
Webscraper portion of code

Resources:
https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25
https://www.selenium.dev/documentation/
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://automatetheboringstuff.com/2e/chapter12/
'''
import time
import bs4, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

import re

class groceryScraper():
    def __init__(self, zipCode):
        self._zipCode = zipCode
        self._wholeFoods = {"url":"https://www.wholefoodsmarket.com/sales-flyer"}
        self._fredMeyer = {"url":"https://www.fredmeyer.com/savings/weeklyad/"}
        self._sprouts = {"url":"https://www.sprouts.com/weekly-ad/"}
        self._safeway = {"url":"https://coupons.safeway.com/weeklyad"}
        self._hMart = {"url": "https://www.hmartus.com/weekly-sale-wa"}

    def initSelenium(self):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        return driver

    def get_wholeFoods(self):
        website = self.initSelenium()
        website.get(self._wholeFoods['url'])
        zipCode = website.find_element(By.ID, 'store-finder-search-bar')
        zipCode.send_keys(self._zipCode)
        website.implicitly_wait(10)
        zipList = website.find_element(By.XPATH, '//*[@id="w-store-finder__search-bar"]/wfm-search-bar/div[2]/div/ul/li[1]')
        website.implicitly_wait(10)
        zipList.click()
        website.implicitly_wait(20)
        checkLoaded = website.find_element(By.ID, 'store-sales')
        page_source = website.page_source
        #print(page_source)

        soup = bs4.BeautifulSoup(page_source, 'html.parser')
        itemname = soup.find_all(class_="w-sales-tile__product")
        itemprice = soup.find_all(class_="w-sales-tile__sale-price w-header3 w-bold-txt")
        saleList = []
        for index in range(0, len(itemname)):
            itemName = itemname[index].text.strip()
            itemPrice = itemprice[index].text.strip()
            saleList.append([itemName, itemPrice])
        print(saleList)
        return saleList

    def get_fredMeyer(self):
        website = self.initSelenium()
        website.get(self._fredMeyer['url'])
        website.implicitly_wait(10)
        iframe = website.find_elements(By.TAG_NAME, 'iframe')
        website.switch_to.frame(iframe[0])
        weeklyAd = website.find_element(By.XPATH, '//*[@id="other_flyer_runs"]/div/div/div/div[2]/table/tbody/tr[1]')
        weeklyAd.click()
        time.sleep(1)
        gridView = website.find_element(By.XPATH, '//*[@id="wishabi-flyerarea"]/div[2]/div/div[1]/div[3]/div/div/div[3]/div/div/div/h4')
        gridView.click()
        time.sleep(3)

        page_source = website.page_source
        print(page_source)

        soup = bs4.BeautifulSoup(page_source, 'html.parser')
        itemname = soup.find_all(class_="item-name")
        itemprice = soup.find_all(class_="item-price")
        for elem in range(0, len(itemname)):
            print(itemname[elem].text.strip(), itemprice[elem].text.strip(), 'new line')


    def get_Sprouts(self):
        website = self.initSelenium()
        website.get('https://www.sprouts.com/stores/')
        website.implicitly_wait(20)
        defaultlocationBar = website.find_element(By.XPATH, '//*[@id="store-map"]')
        defaultlocationBar.click()
        time.sleep(3)

        elem = website.switch_to.active_element

        website.implicitly_wait(20)
        findStore = website.find_element(By.XPATH, '//*[@id="shopping-selector-search-cities"]')
        findStore.send_keys(self._zipCode)
        findStore.send_keys(Keys.ENTER)
        time.sleep(3)

        select = website.find_element(By.XPATH, "//*[text() = 'Select']")
        select.click()
        website.implicitly_wait(10)
        selectAd = website.find_element(By.XPATH, '//*[@id="post-30322"]/div/div/div[2]/div[2]/div[1]/button')
        selectAd.click()
        time.sleep(5)

        page_source = website.page_source
        soup = bs4.BeautifulSoup(page_source, 'html.parser')
        item = soup.find_all('body div div div')
        item2 = soup.findAll('button', {'class': 'inspectBut'})

        for elem in range(0, len(item)):
            print(item[elem].text.strip(), item2[elem], 'new line')

testScraper = groceryScraper(98103)
#testScraper.get_wholeFoods()
#testScraper.get_fredMeyer()
#testScraper.get_Sprouts()

