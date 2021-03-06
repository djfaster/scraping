from lxml import html
import requests
import csv
import time

MainURL = 'https://www.investing.com'
URL = 'https://www.investing.com/indices/nyse-composite-components'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    'Host':'www.investing.com',
    'Referer':'https://www.investing.com'
}

f = open('nyse-symbols.csv', 'w')
with f:
    fnames = ['Name', 'Symbol']
    writer = csv.DictWriter(f, fieldnames=fnames)
    writer.writeheader()
for i in range(1, 5):
    URL = 'https://www.investing.com/indices/nyse-composite-components'    
    if i == 1:
        #print(URL)
        page = requests.get(URL, headers=headers)
        tree = html.fromstring(page.content)
    else:
        URL = URL + '/' + str(i)
        #print(URL)
        page = requests.get(URL, headers=headers)
        tree = html.fromstring(page.content)
    
    count = tree.xpath('//*[@id="cr1"]/tbody/tr')
    countnum = (len(count)) + 1

    for order in range(1, countnum):
        name = tree.xpath('//*[@id="cr1"]/tbody/tr[%s]/td[2]' % order)[0].text_content()  
        href = tree.xpath('//a[text()="%s"]/@href' % name)[0]
        detail = requests.get(MainURL + href, headers=headers)
        detailtree = html.fromstring(detail.content)
        symbol = detailtree.xpath('//meta[@itemprop="tickerSymbol"]/@content')[0]
        #print ('Name = ' +  name + '\n' +'Symbol = ' + symbol )
        
        
        f = open('nyse-symbols.csv', 'a')
        with f:
            fnames = ['Name', 'Symbol']
            writer = csv.DictWriter(f, fieldnames=fnames)
            writer.writerow({'Name' : name, 'Symbol': symbol})
        time.sleep(3)