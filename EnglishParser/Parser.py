#!python3
import urllib.request
from bs4 import BeautifulSoup
from googletrans import Translator
from pymongo import MongoClient

class word():
    eng = ''
    rus = ''
    transcription = ''
    description = ''
    example = ''

def main():
    words = getwords(gethtml('http://studynow.ru/dicta/allwords/'))
    getTranscriptionDescriptionandExample(words)

def gethtml(url):
    response = urllib.request.urlopen(url)
    return response.read()

def getwords(html):
    words = []
    soup = BeautifulSoup(html)
    div = soup.find_all('b')
    count=0
    for d in div:
        if count<8:
            count+=1
            continue
        rus = str(d.next_sibling)
        rus = rus.replace("-", "")
        rus = rus.replace("</b>", "")
        rus = rus.replace(",", "")
        rus = rus.strip()
        eng = str(d)
        eng = eng.replace("<b>","")
        eng = eng.replace("</b>","")
        eng = eng.replace(",","")
        eng = eng.strip()
        buf = word()
        buf.eng = eng
        buf.rus = rus
        words.append(buf)

    return words

def getTranscriptionDescriptionandExample(words):
    for w in words:
        soup = BeautifulSoup(gethtml('http://dictionary.cambridge.org/ru/%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D1%8C/%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9/'+w.eng))
        trans = soup.find_all('span',{"class":"ipa"})
        try:
            res = str(trans[0])
            res = res.replace('<span class="ipa">','')
            res = res.replace('</span>',"")
            res = res.replace('<span class="sp">',"")

        except:
            res = "err"

        try:
            desc = soup.find_all('b', {"class": "def"})
            desc = desc[0].get_text()
            desc = str(desc).replace(":","")
        except:
            desc = "err"

        try:
            examp = soup.find_all('div', {"class": "examp emphasized"})
            examp = examp[0].get_text()
        except:
            examp = "err"

        if res!="err" and desc!="err" and examp!="err":
            w.transcription = res
            w.description = desc
            w.example = examp
            print(w.eng+"="+w.rus+"="+w.transcription+"="+w.description+"="+w.example)
            addWord(w)


def addWord(word):
    res = []
    res.append({"eng":word.eng,"rus":word.rus,"transcription":word.transcription,"description":word.description,"example":word.example})
    client = MongoClient('dbconnect')
    db = client['enclever_test']
    collectionWORDS = db.words
    collectionWORDS.insert(res)

if __name__ == '__main__':
    main()

