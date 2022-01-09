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
        self._wholeFoods = {"url":"https://www.wholefoodsmarket.com/sales-flyer", "name": 'Whole Foods'}
        self._fredMeyer = {"url":"https://www.fredmeyer.com/savings/weeklyad/", "name": "Fred Meyer"}
        self._sprouts = {"url":"https://www.sprouts.com/stores/", "name": "Sprouts"}
        self._safeway = {"url":"https://local.safeway.com/", "name": "Safeway"}
        self._hMart = {"url": "https://www.hmartus.com/weekly-sale-wa", "name": "H Mart"}

    def get_wholeFoods(self):
        return self._wholeFoods

    def get_fredMeyer(self):
        return self._fredMeyer

    def get_sprouts(self):
        return self._sprouts

    def get_safeway(self):
        return self._safeway

    def get_hMart(self):
        return self._hMart

    def initSelenium(self):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        return driver

    def scrape_wholeFoods(self):
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

    def scrape_fredMeyer(self):
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
        saleList = []
        for index in range(0, len(itemname)):
            itemName = itemname[index].text.strip()
            itemPrice = itemprice[index].text.strip()
            saleList.append([itemName, itemPrice])
        print(saleList)
        return saleList

    def scrape_Safeway(self):
        '''
        Work in progress, selenium successfully navigates to correct store and ad but hit a wall scraping data as page source differs fom inspect element
        :return:
        '''
        website = self.initSelenium()
        website.get(self._safeway['url'])
        website.implicitly_wait(20)
        zipCode = website.find_element(By.XPATH, '//*[@id="q"]')
        zipCode.send_keys(self._zipCode)
        zipCode.send_keys(Keys.ENTER)
        time.sleep(2)
        optionOne = website.find_element(By.XPATH, '//*[@id="js-yl-1477"]/article/h3/a/span/span[2]')
        optionOne.click()
        time.sleep(3)
        weeklyAd = website.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[1]/div/div/div/div[2]/a[1]')
        weeklyAd.click()
        time.sleep(8)
        website.get(r'https://coupons.safeway.com/weeklyad/')
        print(website.current_url)


    def scrape_Sprouts(self):
        '''
        Work in progress, selenium successfully navigates to correct store and ad but hit a wall scraping data as page source differs fom inspect element
        :return:
        '''
        website = self.initSelenium()
        website.get(self._sprouts['url'])
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
        inspect_page = website.execute_script("return document.documentElement.innerHTML")
        print(inspect_page)
        soup = bs4.BeautifulSoup(page_source, 'html.parser')
        item = soup.find_all('body div div div')
        item2 = soup.findAll('button', {'class': 'inspectBut'})

        for elem in range(0, len(item)):
            print(item[elem].text.strip(), item2[elem], 'new line')

    def scrape_hMart(self):
        pass

testScraper = groceryScraper(98103)
#testScraper.get_wholeFoods()
#testScraper.get_fredMeyer()
#testScraper.scrape_Sprouts()
#testScraper.get_Safeway()

