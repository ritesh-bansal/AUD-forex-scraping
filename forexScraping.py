from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json

url = 'https://www.investing.com/currencies/single-currency-crosses'

pair = []
bid = []
ask = []
high = []
low = []
chg = []
chgPer = []
time = []

symbols = ['USD', 'EUR', 'JPY', 'GBP', 'CAD', 'CHF', 'CNH', 'SEK', 'NZD', 'INR']
options = Options()
options.headless = True
driver = webdriver.Chrome('D:/chromedriver.exe', options=options)
driver.get(url)

dropdown = driver.find_element_by_css_selector('#symbols')
dropdown.send_keys('AUD')
sleep(1)

soup = BeautifulSoup(driver.page_source, 'lxml')
table = soup.find('table', class_="genTbl closedTbl crossRatesTbl elpTbl elp20")
rows = table.find_all('tr')

for row in rows[1:]:
    pair.append(str(row.find_all('td')[1].text.replace('\n', '')))
    bid.append(str(row.find_all('td')[2].text.replace('\n', '')))
    ask.append(str(row.find_all('td')[3].text.replace('\n', '')))
    high.append(str(row.find_all('td')[4].text.replace('\n', '')))
    low.append(str(row.find_all('td')[5].text.replace('\n', '')))
    chg.append(str(row.find_all('td')[6].text.replace('\n', '')))
    chgPer.append(str(row.find_all('td')[7].text.replace('\n', '')))
    time.append(str(row.find_all('td')[8].text.replace('\n', '')))

forex = []
for i, j, k, l, m, n, o, p in zip(pair, bid, ask, high, low, chg, chgPer, time):
    myDict = {'Pair': i, 'Bid': j, 'Ask': k, 'High': l, 'Low': m, 'Chg': n, 'Chg%': o, 'Time': p}
    forex.append(myDict)

forex = {"forex": [f for f in forex for ele in symbols if ele in f['Pair']]}
print(forex)

with open('forex.json', 'w') as fout:
    json.dump(forex, fout)