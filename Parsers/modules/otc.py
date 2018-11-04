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
    url = 'https://otc.ru/tenders/?SearchForm.MinContractGuarantee=0&SearchForm.MaxContractGuarantee=1000000000000&SearchForm.DatePublishedFrom= '+str(date_t)+'&SearchForm.DatePublishedTo= '+str(date_t)+'&SearchForm.State=1&SearchForm.DocumentSearchEnabled=True&SearchForm.WithdrawnSearchEnabled=False&SearchForm.HasApplications=on&SearchForm.CurrencyCode=643&SearchForm.SectionIds=2&SearchForm.SectionIds=3&SearchForm.SectionIds=7&SearchForm.SectionIds=9&SearchForm.SectionIds=10&SearchForm.SectionIds=6&SearchForm.SectionIds=1&SearchForm.SectionIds=99&SearchForm.SectionIds=100&SearchForm.SectionIds=98&SearchForm.SectionIds=96&SearchForm.SectionIds=97&SearchForm.SectionIds=91&SearchForm.SectionIds=94&SearchForm.SectionIds=89&SearchForm.SectionIds=90&SearchForm.SectionIds=92&SearchForm.SectionIds=93&SearchForm.SectionIds=101&SearchForm.SectionIds=102&SearchForm.SectionIds=103&SearchForm.SectionIds=104&SearchForm.SectionIds=105&SearchForm.SectionIds=107&SearchForm.SectionIds=108&SearchForm.SectionIds=109&SearchForm.SectionIds=110&SearchForm.SectionIds=111&SearchForm.SectionIds=112&SearchForm.SectionIds=113&SearchForm.SectionIds=106&SearchForm.SectionIds=114&SearchForm.SectionIds=115&SearchForm.SectionIds=116&SearchForm.SectionIds=117&SearchForm.SectionIds=118&SearchForm.SectionIds=119&SearchForm.SectionIds=120&SearchForm.SectionIds=121&SearchForm.OrganizationLevels=Fz223&SearchForm.KeywordsAndJoinEnabled=True&FilterData.SortingField=DatePublished&FilterData.SortingDirection=Asc&FilterData.PageSize=20&FilterData.PageIndex=1&'
    '''
    # Получаем страницу
    r = requests.get(
        url=url,
        headers=headers
        )
        '''
    chrom_path = 'C:\\Users\\m.kilinskii\\Desktop\\chromedriver_win32\\chromedriver.exe'  # Хромовский веб драйвер
    driver = webdriver.Chrome(chrom_path)
    driver.get(url)
    # html = driver.page_source

    search = driver.find_element_by_xpath('.//span[@class="filter-btn Search"]')  # driver.find_element_by_class_name('btn Search')
    driver.execute_script("arguments[0].click();", search)
    # search.click()
    html = driver.page_source
    # print(html)
    driver.close()


    s = BeautifulSoup(html, "html.parser")
    xmlData = s.find_all("div", class_='result_item bootstrap-iso')
    #print(xmlData)

    spisok = []
    for rw in xmlData:
        # print(rw)
        guarantee = rw.find("div", class_='guarantee-containter').get_text()
        # print(guarantee)
        # print(rw.find_all('a')[9])
        # print(rw)
        try:
           if len(rw.find_all('a')[9].get_text()) == 11:
               purchase = rw.find_all('a')[9].get_text()
               #print(purchase)
               spisok.append(['ОТС',None,purchase,guarantee])
               #print(spisok)
        except:

             continue

    return spisok





if __name__ == '__main__':


    date_t = datetime(2017,11,20)
    # print (date_t)
    startparseOTC (date_t)
