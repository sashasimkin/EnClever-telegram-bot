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
    addEngWords(words)
    #Translate()
    #printDbDoc()

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

def Translate():
    client = MongoClient('46.101.216.92', port=27017, password='Nlx74OMEgacFnxSS', authSource='enclever_test')
    db = client['enclever_test']
    collectionWORDS = db.words
    translator = Translator()
    cursor = collectionWORDS.find()
    count = 0
    for doc in cursor:
        try:
            buf = (translator.translate(str(doc['eng']), dest='ru')).text
        finally:
            buf = "error"
        collectionWORDS.update_one({'_id': doc['_id']}, {
            '$set': {
                'rus': buf
            }
        }, upsert=False)
        count += 1
        print (str(count)+" = "+(translator.translate(doc['eng'], dest='ru')).text)



def addEngWords(words):
    res=[]
    for w in words:
        res.append({"eng":w.eng,"rus":w.rus})

    client = MongoClient('46.101.216.92', port=27017 , password='Nlx74OMEgacFnxSS', authSource='enclever_test')
    db = client['enclever_test']
    collectionWORDS = db.words
    collectionWORDS.insert_many(res)
    cursor = collectionWORDS.find()
    for doc in cursor:
        print(doc)

def printDbDoc():
    client = MongoClient('46.101.216.92', port=27017, password='Nlx74OMEgacFnxSS', authSource='enclever_test')
    db = client['enclever_test']
    collectionWORDS = db.words
    cursor = collectionWORDS.find()
    for doc in cursor:
        print(doc['_id'])
        print(doc['eng'])

if __name__ == '__main__':
    main()

