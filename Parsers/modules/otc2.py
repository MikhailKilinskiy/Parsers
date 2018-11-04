import json
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime


def startparseOTC(date):
    date_t = date.strftime('%d.%m.%Y')
    headers = {'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               'accept - encoding': 'gzip, deflate, br',
               'accept - language':'en - US, en; q = 0.9',
               'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
    url = 'https://otc.ru/tenders/?SearchForm.MinContractGuarantee=1&SearchForm.MaxContractGuarantee=1000000000&SearchForm.DatePublishedFrom='+str(date_t)+'&SearchForm.DatePublishedTo='+str(date_t)+'&SearchForm.State=0&SearchForm.DocumentSearchEnabled=True&SearchForm.WithdrawnSearchEnabled=True&SearchForm.HasApplications=on&SearchForm.CurrencyCode=643&SearchForm.SectionIds=2&SearchForm.SectionIds=3&SearchForm.SectionIds=7&SearchForm.SectionIds=9&SearchForm.SectionIds=10&SearchForm.SectionIds=6&SearchForm.SectionIds=1&SearchForm.SectionIds=99&SearchForm.SectionIds=100&SearchForm.SectionIds=98&SearchForm.SectionIds=96&SearchForm.SectionIds=97&SearchForm.SectionIds=91&SearchForm.SectionIds=88&SearchForm.SectionIds=94&SearchForm.SectionIds=89&SearchForm.SectionIds=90&SearchForm.SectionIds=92&SearchForm.SectionIds=93&SearchForm.SectionIds=87&SearchForm.SectionIds=95&SearchForm.SectionIds=86&SearchForm.SectionIds=101&SearchForm.SectionIds=102&SearchForm.SectionIds=103&SearchForm.SectionIds=104&SearchForm.SectionIds=105&SearchForm.SectionIds=107&SearchForm.SectionIds=108&SearchForm.SectionIds=109&SearchForm.SectionIds=110&SearchForm.SectionIds=111&SearchForm.SectionIds=112&SearchForm.SectionIds=113&SearchForm.SectionIds=106&SearchForm.SectionIds=114&SearchForm.SectionIds=115&SearchForm.SectionIds=116&SearchForm.SectionIds=117&SearchForm.SectionIds=118&SearchForm.SectionIds=119&SearchForm.SectionIds=120&SearchForm.SectionIds=121&SearchForm.OrganizationLevels=Fz223&SearchForm.KeywordsAndJoinEnabled=True&FilterData.SortingField=DatePublished&FilterData.SortingDirection=Desc&FilterData.PageSize=50&FilterData.PageIndex=1&'
    # '+str(date_t)+'
    # Получаем страницу
    r = requests.get(
        url=url,
        headers=headers
        )

    # print(url)
    s = BeautifulSoup(r.text, "html.parser")
    xmlData = s.find_all("div", class_='result_item bootstrap-iso')
    # print(xmlData)


    for rw in xmlData:
        # print(rw)
        guarantee = rw.find("div", class_='guarantee-containter').get_text()
        p = rw.find_all('a')
        for i, it in enumerate(p):
            if it.get_text() == 'ЕИС':
                purchase=p[i+1].get_text()
                # print(purchase)
                spisok = ['ОТС', None, purchase, guarantee]
                # print(spisok)
                yield spisok



'''

if __name__ == '__main__':


    date_t = datetime(2016,12,6)
    # print (date_t)
    i = 0
    for d in startparseOTC (date_t):
        i += 1
        print(i)
        print(d)
        '''





