
import json
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime


def startparseRoseltorg(pagenum, headers, date):
    date_t = datetime.strptime(date, '%d.%m.%Y').strftime('%d.%m.%y')
    # Получаем страницу
    r = requests.post(
        url='https://www.roseltorg.ru/procedures/search?query_field=&source%5B%5D=2&source%5B%5D=3&source%5B%5D='
            '5&source%5B%5D=6&source%5B%5D=8&source%5B%5D=9&source%5B%5D=11&source%5B%5D=14&source%5B%5D=12&customer='
            '&start_price=&end_price=&currency=all&address=&start_date_published='+str(date_t)+'&end_date_published=&start_date_requests='
            '&end_date_requests=&guarantee_start_price=&guarantee_end_price=&deposit=1&page=&form_id=searchp_form&from=' + str(
            pagenum*10),
        headers=headers)

    s = BeautifulSoup(r.text, "html.parser")

    xmlData = s.find_all("div", class_='g-proc-num')
    xmlData2 = s.find_all("div", class_='w-addit-b')
    spisok = []

    global nexist
    if len(xmlData) == 0:
        nexist = False
    else:
        for rw in xmlData:
            href = rw.contents[1]['href']
            p = rw.find_all("a")[0].get_text().replace('№','').replace(' ','').replace('\xa0','')
            purchase = p[:p.find('(')]
            spisok.append(['Россельторг',href,purchase])

        guar = []
        for rw2 in xmlData2:
            g = rw2.find_all("p")[1].get_text()
            guarantee = g[g.find('Обеспечение контракта'):g.find('₽')].replace('Обеспечение контракта:\n', '').strip().split('\n')

            if guarantee != ['']:
                guar.append(guarantee)
            else:
                continue
        bg = []
        for i, s in zip (guar, spisok):
             s.append (i[0])
             # print (s)
             bg.append(s)

        return bg

'''
if __name__ == '__main__':
    headers = {'Accept': "*/*",
               'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
               'X-Requested-With': 'XMLHttpRequest'
               }

    date_t = datetime(2017,1,1).strftime('%d.%m.%Y')
    print (date_t)
    print (startparseRoseltorg (0, headers, date_t))
    '''




