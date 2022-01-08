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
        time.sleep(3)
        gridView = website.find_element(By.XPATH, '//*[@id="wishabi-flyerarea"]/div[2]/div/div[1]/div[3]/div/div/div[3]/div/div/div/h4')
        gridView.click()
        time.sleep(3)

        page_source = website.page_source
        #print(page_source)

        soup = bs4.BeautifulSoup(page_source, 'html.parser')
        itemname = soup.find_all(class_="item-name")
        itemprice = soup.find_all(class_="item-price")
        for elem in range(0, len(itemname)):
            print(itemname[elem].text.strip(), itemprice[elem].text.strip(), 'new line')

    def get_Sprouts(self):
        website = self.initSelenium()
        website.get(self._sprouts['url'])
        website.implicitly_wait(60)
        try:
            defaultlocationBar = website.find_element(By.ID, '#postal-input')
            ##postal-input
            print('found default location bar', defaultlocationBar)
            defaultlocationBar.click()
        except NoSuchElementException:
            pass
        try:
            emptylocationBar = website.find_element(By.XPATH, '//*[@id="postal-input"]')
            print('found empty location bar', emptylocationBar)
            emptylocationBar.send_keys(self._zipCode)
            #//*[@id="postal-input"]
        except NoSuchElementException:
            pass

        try:
            secondlocationBar = website.find_element(By.XPATH, '//*[@id="storeNavigationBtn"]/div/div[2]/h3[2]')
            print('found second location bar', secondlocationBar)
            secondlocationBar.click()
        except NoSuchElementException:
            pass

        #XPATH //*[@id="store-name"]
        #ID#store-name
        #locationBar.click()
        website.implicitly_wait(10)
        iframe = website.find_elements(By.TAG_NAME, 'iframe')
        print(iframe)
        website.switch_to.frame(iframe[0])
        try:
            zipCode = website.find_element(By.ID, '#shopping-selector-search-cities')
            zipCode.send_keys(self._zipCode)
            print('found zipcode enter', zipCode)
        except NoSuchElementException:
            pass
        time.sleep(30)



testScraper = groceryScraper(98103)
#testScraper.get_wholeFoods()
#testScraper.get_fredMeyer()
testScraper.get_Sprouts()

# random junk
# print(soup)
# zipList = Select(website.find_element(By.XPATH, '//*[@id="w-store-finder__search-bar"]/wfm-search-bar/div[2]/div'))
##w-store-finder__search-bar > wfm-search-bar > div.wfm-search-bar--list_container > div > ul > li:nth-child(1) > span
# zipList.select_by_index(0)
# print(zipList.page_source)
# website.implicitly_wait(20)
# print(website.page_source)
# res = requests.get('https://www.wholefoodsmarket.com/sales-flyer?store-id=10103')
# res.raise_for_status()
# soup = bs4.BeautifulSoup(res.text, 'html.parser')