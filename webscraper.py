#Code for webscraping portion of project
import bs4, requests
from selenium import webdriver


driver = webdriver.Chrome()

driver.get("http://selenium.dev")

driver.quit()


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

wholefoods()