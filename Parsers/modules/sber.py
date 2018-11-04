
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree
import time

def startparseSber(pagenum, headers, date):
    # Процедура для получения списка ссылок на закупки сбера
    # установим xml фильтр
    # xFilter = '<elasticrequest><size>300</size><from>'+str(10*pagenum)+'</from></elasticrequest>'
    xFilter = '<elasticrequest><filters><PublicDate><minvalue>'+str(date)+' 00:00</minvalue><maxvalue></maxvalue></PublicDate></filters><size>300</size><from>' + str(300*pagenum) + '</from></elasticrequest>'

    # Параметры запроса
    payload = {"xmlData": xFilter,
               "orgId": 0}

    # Получаем страницу
    r = requests.post(
        url= 'http://utp.sberbank-ast.ru/Trade/SearchQuery/PurchaseList', #BidList
        data=payload,
        headers=headers)

    data = json.loads(r._content)

    global nextlist
    if data['result'] == 'error':
        nextlist == False
    else:
        data = json.loads(r._content)
        xml_table = data['data']['Data']['data']
        d2 = json.loads(xml_table)

        d3 = d2['hits']['hits']
        # print (d3)
        if d3 == None:
            nextlist == False
        else:
            links = ['http://utp.sberbank-ast.ru/Trade/NBT/PurchaseView/41/0/0/'+str(id['_id']) for id in d3]

            return links

#########################################################################

def sberParser(sberurl):
    # Парсит одну процедуру
    f = requests.get(sberurl)
    bsObj = BeautifulSoup(f.text, "html.parser")
    xmlData = bsObj.find_all("input", id="xmlData")[0]['value']
    # print (xmlData)
    tree = etree.XML(xmlData)
    # print(tree.findall(".//BidContractCoverDemand"))
    purchase = str (tree.findall(".//PurchaseOOSregistrationNumber")[0].text)
    try:
        guarantee = str (tree.findall(".//BidContractCoverDemand")[0].text)
    except:
        guarantee = 'No'

    # print (tree.findall(".//PurchaseOOSregistrationNumber"))

    spisok = ['Сбербанк', sberurl, purchase, guarantee]

    return spisok

'''
if __name__ == '__main__':

    #u = "http://utp.sberbank-ast.ru/Trade/NBT/PurchaseView/41/0/0/225661"
    #print (sberParser(u))

    headers = {'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
               'X-Requested-With': 'XMLHttpRequest'
               }

    #############################################################################################################
    print('------- СБЕРБАНК --------')
    # Парсим сбербанк
    nextlist = True
    n = 0
    while nextlist == True:
        try:
            print('Сбербанк - Страница {n}'.format(n=str(n)))
            for s in startparseSber(n, headers):  # Для каждой ссылке на странице
                # print(s)

                try:
                    print (sberParser(s))          # Получаем список полей
                    time.sleep(5)
                except BaseException as e:
                    print (e)
                    continue

            n += 1
            time.sleep(5)
        except BaseException as err:
            print (err)
            break
            '''







