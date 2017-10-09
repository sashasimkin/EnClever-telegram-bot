from bs4 import BeautifulSoup
from urllib.request import *

req_word = 'car'

url = 'http://lelang.ru/?s=%s' %req_word

def get_html(url):
    req = Request(url)
    html = urlopen(req).read()
    return html

def main():
    opener = build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0')]
    install_opener(opener)
    for i in range(1,2):
        html = get_html(url)
        soup = BeautifulSoup(html,'html.parser')
        list = soup.select('div.post_content a[href]')
        for a in list:
            print(a.get('href'))
main()