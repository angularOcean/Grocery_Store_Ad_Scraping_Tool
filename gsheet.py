'''
Spreadsheet portion of code
Utilizes gspread to create a workbook in google drive with worksheets for each store's sales information

Resources:
Enable API Access: https://docs.gspread.org/en/latest/oauth2.html#enable-api-access


'''

import gspread
gc = gspread.oauth(
    credentials_filename= r'C:\CS_Projects\credentials.json',
    authorized_user_filename= r'C:\CS_Projects\authorized_user.json'
)

from datetime import date
today = date.today()

import time

from webscraper import groceryScraper

class dataBuilder():
    '''This class builds the spreadsheets, taking a zipcode for its only input in order to find the nearest stores to that location'''
    def __init__(self, zipCode):
        self._data = groceryScraper(zipCode)
        self._mainFileName = "Grocery Sales for " + str(date.today())
        self._mainFile = gc.create(self._mainFileName)

    def deleteSheet(self, name):
        self._mainFile.del_worksheet(name)

    def generateSheet(self, storeName):
        '''This method takes the name of a store it has a webscraper for and calls the webscraper to grab the sales data
        Right now it only accepts Whole Foods and Fred Meyer as they are the only scrapers that work. '''
        if storeName == "Whole Foods":
            name = self._data.get_wholeFoods()["name"]
            print("Retrieving Sales Data")
            storeData = self._data.scrape_wholeFoods()


        elif storeName == "Fred Meyer":
            name = self._data.get_fredMeyer()["name"]
            print("Retrieving Sales Data")
            storeData = self._data.scrape_fredMeyer()

        else:
            return "Sorry there is no web scraper available for that store!"

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



testClass = dataBuilder(98103)
testClass.generateSheet("Whole Foods")
testClass.generateSheet("Fred Meyer")
