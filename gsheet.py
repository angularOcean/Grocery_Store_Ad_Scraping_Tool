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

from webscraper import groceryScraper

class dataBuilder():
    def __init__(self, zipCode):
        self._data = groceryScraper(zipCode)
        self._mainFileName = "Grocery Sales for " + str(date.today())
        self._mainFile = gc.create(self._mainFileName)

    def wholeFoodsSheet(self):
        print("Generating Whole Foods Worksheet")
        createSheet = self._mainFile.add_worksheet("Sales for Whole Foods", rows="100", cols="20")
        wf = gc.open(self._mainFileName).worksheet("Sales for Whole Foods")
        print("Retrieving Sales Data")
        wholeFoodData = self._data.get_wholeFoods()
        count = 2
        print("Populating worksheet")
        for element in wholeFoodData:
            wf.insert_row(element, count)
            count += 1
'''
def sheetBuilder(zipCode):
    fileName = "Grocery Sales for " + str(today)
    mainFile = gc.create(fileName)
    wfSheet = mainFile.add_worksheet("Sales for Whole Foods", rows = "100", cols = "20")
    wf = gc.open(fileName).worksheet("Sales for Whole Foods")
    getData = groceryScraper(zipCode)
    wholeFoodData = getData.get_wholeFoods()
    count = 2
    for element in wholeFoodData:
        wf.insert_row(element,count)
        count +=1
'''


#sheetBuilder(98103)
testClass = dataBuilder(98103)
testClass.wholeFoodsSheet()