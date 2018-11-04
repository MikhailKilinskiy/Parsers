

import json
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
from datetime import timedelta, datetime

def startparseETP(pagenum, type, date):

    if type == 'OK': # Открытый конкурс

        # Параметры запроса
        payload = {
            "_orm_PageID": "5FBADDEAC01D2893",
            "_orm_PageURL": "http://223etp.zakazrf.ru/NotificationOK/Index",
            "_orm_ClientType": "Browser",
            "SortColumn5FBADDEAC01D2893": "ID",
            "Filter.PublicationDateFrom": str(date),
            "SortColumnDesc5FBADDEAC01D2893": 1,
            "PageNumber5FBADDEAC01D2893": pagenum,
            "PageSize5FBADDEAC01D2893": 20,
            "PageNumberView15FBADDEAC01D2893": pagenum,
            "PageCountView15FBADDEAC01D2893": 21,
            "TotalRowsView15FBADDEAC01D2893": 410,
            "Filter.SelectedTabPage": 0,
            "_orm_SerializableTableKey": "BD34D1A4A5335446"
                   }
        # print (payload)
        # Получаем страницу
        r = requests.post(
            url= 'http://223etp.zakazrf.ru/NotificationOK?IsPartialView=1&IsTableContentOnlyRequest=1',
            data=payload,
            headers={
                'X-Requested-With': 'XMLHttpRequest'
            }
        )

    elif type == 'ZP': # Запрос предложений

        # Параметры запроса
        payload = {
            "_orm_PageID": "5FBADDEA4D5F3CB4",
            "_orm_PageURL": "http://223etp.zakazrf.ru/NotificationZP/Index",
            "_orm_ClientType": "Browser",
            "SortColumn5FBADDEA4D5F3CB4": "ID",
            "Filter.PublicationDateFrom": str(date),
            "SortColumnDesc5FBADDEA4D5F3CB4": 1,
            "PageNumber5FBADDEA4D5F3CB4": pagenum,
            "PageSize5FBADDEA4D5F3CB4": 20,
            "PageNumberView5FBADDEA4D5F3CB4": pagenum,
            "PageCountView5FBADDEA4D5F3CB4": 21,
            "TotalRowsView5FBADDEA4D5F3CB4": 410,
            "Filter.SelectedTabPage": 0,
            "_orm_SerializableTableKey": "BD34D1A4BAD4FEF4"
        }
        # print (payload)
        # Получаем страницу
        r = requests.post(
            url='http://223etp.zakazrf.ru/NotificationZP?IsPartialView=1&IsTableContentOnlyRequest=1',
            data=payload,
            headers={
                'X-Requested-With': 'XMLHttpRequest'
            }
        )

    s = BeautifulSoup(r.text, "html.parser")
    links = s.find_all('a', href=True)
    global nextlist
    # print (links)

    if len (links) != 0:
        link_list = []
        for link in links:
            L = 'http://223etp.zakazrf.ru' + str(link['href'])
            # print (L)
            link_list.append(L)

        return link_list
    else:
        nextlist == False

#########################################################################

def etpParser(etprurl):
    # Парсит одну процедуру
    f = requests.get(etprurl)
    bsObj = BeautifulSoup(f.text, "html.parser")
    number = bsObj.find_all(class_='td-value')
    number2 = bsObj.find_all("tr")

    for n in number2:
        #print(n.find(class_='td-value'))
        #print(n.find(class_='td-label'))

        try:
            if n.find(class_='td-label').get_text().find('Реестровый номер') != -1:
                purchase = n.find(class_='td-value').get_text()

            if n.find(class_='td-label').get_text().find('Дополнительная информация') != -1:
                guarantee = n.find(class_='td-value').get_text()
        except AttributeError:
            continue


    spisok = ['223ETP.ZAKAZRF', etprurl, purchase, guarantee]

    return spisok


'''
if __name__ == '__main__':

    # print (etpParser('http://223etp.zakazrf.ru/NotificationOK/id/639'))


    #############################################################################################################
    date_t = datetime(2017, 10, 19).strftime('%d.%m.%Y')
    print('------- ЕТП --------')
    # Парсим ЕТП
    nextlist = True
    n = 1
    while nextlist == True:
        for type in ['ZP','OK']:
            try:
                print('ЕТП - Страница {n}'.format(n=str(n)))

                for s in startparseETP(n, type, date_t):  # Для каждой ссылке на странице
                    print(etpParser(s))  # Получаем список полей и вставляем в таблицу
                    time.sleep(3)

                n += 1
                time.sleep(5)
            except BaseException as err:
                print(err)
                break
                '''



