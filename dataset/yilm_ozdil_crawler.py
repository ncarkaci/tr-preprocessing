import urllib.request
import requests
from lxml import html
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

def fetch():
    start = 1
    end = 257
    main_url = 'http://www.hurriyet.com.tr/yazarlar/yilmaz-ozdil/?p='

    page_url_list = []

    for page_num in range(start,end):
        page_url = main_url+str(page_num)
        print ('Fetch url : '+page_url)
        page_url_list.append(page_url)

        page = urllib.request.urlopen(page_url)

        url_list = []
        soup = BeautifulSoup(page)
        for link in soup.findAll("a"):
            sublink = link.get("href")

            if (sublink != None):

                url = 'http://www.hurriyet.com.tr'+sublink
                if (url not in url_list):
                    url_list.append(url)

        with open('out.txt', 'a') as file_handler:
            for item in url_list:
                file_handler.write("{}\n".format(item))


# Proxy
proxy = {
    'user': '',  # proxy username
    'pass': '',  # proxy password
    'host': "",  # proxy host (Kullanılmayacaksa boş bırak)
    'port': 8080  # proxy port
}

# Set variables
proxy['host'] = "5.196.218.190"  # Örnek proxy sunuxu adresi
user_agent = UserAgent()
agentHeader = {'User-Agent': user_agent.random}


from pyvirtualdisplay import Display
from selenium import webdriver

with open('out2.txt') as f:
    lines = f.readlines()

# Hide firefox browser
display = Display(visible=0, size=(1024, 768))
display.start()
print('Arka planda çalışma uygulaması başlatıldı.')

# Start browser
browser = webdriver.Firefox()  # or add to your PATH
browser.set_window_size(1024, 768)  # optional
print('Firefox browser başlatıldı.')

filenum = 1
for url in lines:
    print (url)

    filename = url.replace('http://www.hurriyet.com.tr/', "")+'.txt'
    filename = filename.replace('/',"")
    filename = filename.replace('\\',"")

    fpath = os.getcwd()+'/'+filename

    if (not os.path.isfile(fpath)):

        # Set URL
        browser.get(url)
        browser.save_screenshot('screen.png')
        print('Bağlantı kuruldu.')

        # Set text
        content = browser.find_element_by_xpath('//div[@class="article-content news-text"]').text
        print ('İçerik alındı')
        with open(filename, 'w') as file_handler:
            file_handler.write(content)
        print ('İçerik dosyay yazıldı.')
