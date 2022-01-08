'''
Webscraper portion of code

Resources:
https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25
https://www.selenium.dev/documentation/
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
https://automatetheboringstuff.com/2e/chapter12/
'''

import bs4, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service




#driver.get("http://selenium.dev")


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
        #print(soup)
        #zipList = Select(website.find_element(By.XPATH, '//*[@id="w-store-finder__search-bar"]/wfm-search-bar/div[2]/div'))
        ##w-store-finder__search-bar > wfm-search-bar > div.wfm-search-bar--list_container > div > ul > li:nth-child(1) > span
        #zipList.select_by_index(0)
        #print(zipList.page_source)
        #website.implicitly_wait(20)
        #print(website.page_source)
        #res = requests.get('https://www.wholefoodsmarket.com/sales-flyer?store-id=10103')
        #res.raise_for_status()
        #soup = bs4.BeautifulSoup(res.text, 'html.parser')
        itemname = soup.find_all(class_="w-sales-tile__product")
        itemprice = soup.find_all(class_="w-sales-tile__sale-price w-header3 w-bold-txt")
        count = 0
        for elem in range(0, len(itemname)):
            print(itemname[elem].text.strip(), itemprice[elem].text.strip(), count)
            count += 1
        print(count)


##form-group--68
#other_flyer_runs > div > div > div > div.other_flyer_runs_wrapper > table > tbody > tr.flyer_run_762661.clickable > td.info
#price = getAmazonPrice('https://www.amazon.com/Life-Extension-Melatonin-300-Capsules/dp/B000X9QZZ2/')
#print('The price is ' + price)
def testFunction():
    res = requests.get('https://nostarch.com')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('body div div section div div section  div div article header a')
    res.raise_for_status()
    noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    count = 0
    for elem in elems:
        print(elem.text.strip(), count)
        count +=1
    #print(noStarchSoup)
    return type(noStarchSoup)

#/html/body/div[9]/div/section/div/section[1]/div/div[2]/section/div/div[1]/div[1]/article/header/h2/a
#print(testFunction())

def fredmeyer():
    res = requests.get('https://www.fredmeyer.com/savings/weeklyad/')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('body div a')
    count = 0
    for elem in elems:
        print(elem.text.strip(), count)
        count +=1
    print(count)
    #//*[@id="wrapper"]/div[8]/div/div[2]/div[1]/ul/li[1]/div[1]/div/a/img
    #/html/body/div[3]/div[8]/div/div[2]/div[1]/ul/li[1]/div[1]/div/a/img

#fredmeyer()

def wholefoods():
    res = requests.get('https://www.wholefoodsmarket.com/sales-flyer?store-id=10103')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    itemname = soup.find_all(class_="w-sales-tile__product")
    itemprice = soup.find_all(class_="w-sales-tile__sale-price w-header3 w-bold-txt")
    count = 0
    for elem in range(0, len(itemname)):
        print(itemname[elem].text.strip(), itemprice[elem].text.strip(), count)
        count +=1
    print(count)
    #/html/body/main/article[3]/section[2]/div/ul/li[2]/div[2]/div[2]/div/span[2]

testScraper = groceryScraper(98103)
testScraper.get_wholeFoods()