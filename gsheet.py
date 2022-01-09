'''
Spreadsheet portion of code

Resources:
Enable API Access: https://docs.gspread.org/en/latest/oauth2.html#enable-api-access


'''

import gspread
gc = gspread.oauth(
    credentials_filename= r'C:\Users\herak\PycharmProjects\Grocery_Scraper\credentials.json',
    authorized_user_filename= r'C:\Users\herak\PycharmProjects\Grocery_Scraper\authorized_user.json'
)

from datetime import date
today = date.today()

import time

from webscraper import groceryScraper

class dataBuilder():
    def __init__(self, zipCode):
        self._data = groceryScraper(zipCode)
        self._mainFileName = "Grocery Sales for " + str(date.today())
        self._mainFile = gc.create(self._mainFileName)

    def deleteSheet(self, name):
        self._mainFile.del_worksheet(name)

    def generateSheet(self, storeName):
        if storeName == "Whole Foods":
            name = self._data.get_wholeFoods()["name"]
            print("Retrieving Sales Data")
            storeData = self._data.scrape_wholeFoods()


        elif storeName == "Fred Meyer":
            name = self._data.get_fredMeyer()["name"]
            print("Retrieving Sales Data")
            storeData = self._data.scrape_fredMeyer()

        wsName = "Sales for " + name
        print("Generating " + name + " Worksheet")
        self._mainFile.add_worksheet(wsName, rows="100", cols="20")
        wf = gc.open(self._mainFileName).worksheet(wsName)

        print("Populating worksheet")
        headerRow = ["Item Name", "Price"]
        wf.insert_row(headerRow, 1)
        count = 2
        for element in storeData:
            time.sleep(2)
            wf.insert_row(element, count)
            count += 1

    def wholeFoodsSheet(self):
        print("Generating Whole Foods Worksheet")
        createSheet = self._mainFile.add_worksheet("Sales for Whole Foods", rows="100", cols="20")
        wf = gc.open(self._mainFileName).worksheet("Sales for Whole Foods")
        print("Retrieving Sales Data")
        salesData = self._data.get_wholeFoods()
        count = 2
        print("Populating worksheet")
        for element in salesData:
            wf.insert_row(element, count)
            count += 1

    def fredMeyerSheet(self):
        print("Generating Fred Meyer Worksheet")
        createSheet = self._mainFile.add_worksheet("Sales for Fred Meyer", rows="100", cols="20")
        wf = gc.open(self._mainFileName).worksheet("Sales for Fred Meyer")
        print("Retrieving Sales Data")
        salesData = self._data.get_fredMeyer()
        count = 2
        print("Populating worksheet")
        for element in salesData:
            wf.insert_row(element, count)
            time.sleep(1)
            count += 1


testClass = dataBuilder(98103)
testClass.generateSheet("Whole Foods")
testClass.generateSheet("Fred Meyer")
