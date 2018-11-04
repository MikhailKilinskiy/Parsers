
import json
import requests
import time
import modules.sber as sb
import modules.etp as etp
import modules.roseltorg as rs
import modules.otc2 as otc
import pyodbc
from threading import *
from datetime import timedelta, datetime

lock = Lock() # Объект блокировки

# Соединение с базой
connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=*******;'
                            'Database=OOS_DWH;'
                            'Trusted_Connection=yes')

def sql_insert (sp):
    # Вставка в БД
    cursor = connection.cursor()
    SQLCommand = ("INSERT INTO [OOS_DWH].[dbo223].[ContractGuaranteeParser]"
                  "([ETP],[url],[PurchaseNumber],[ContractGuaranteeText])"
                  "VALUES (?,?,?,?)")
    Values = sp
    cursor.execute(SQLCommand, Values)
    connection.commit()

    print (sp)

def purchase_distinct(number):
    # Проверка если процедура уже была загружена
    cursor = connection.cursor()
    SQLCommand = ("SELECT PurchaseNumber FROM [OOS_DWH].[dbo223].[ContractGuaranteeParser] WHERE PurchaseNumber = ?")
    Values = number
    cursor.execute(SQLCommand, Values)
    data = cursor.fetchall()

    if len(data) == 0:
        return True
    else:
        return False


def get_date(e):
    cursor = connection.cursor()
    SQLCommand = ("SELECT ISNULL (MAX (PN.[PublicationDateTime]),'20160801') as [PublicationDateTime] "
                  "FROM [OOS_DWH].[dbo223].[ContractGuaranteeParser] CGP with (nolock) "
                  "JOIN [parserFTP223FL].[dbo].[PurchaseNotice] PN with (nolock) "
                  "ON PN.[RegistrationNumber] = CGP.PurchaseNumber "
                  "WHERE PN.[PublicationDateTime] <= DATEADD (d, -20, GETDATE())"
                  "AND ETP = ? ")

    Values = e
    cursor.execute(SQLCommand, Values)

    max_date = cursor.fetchone()[0]
    print(max_date.strftime('%d.%m.%Y'))

    return max_date.strftime('%d.%m.%Y')

def sql_truncate():

    cursor = connection.cursor()
    SQLCommand = ("truncate table [OOS_DWH].[dbo223].[ContractGuaranteeParser]")
    cursor.execute(SQLCommand)
    connection.commit()

    print('----------- TABLE TRUNCATE SUCESSFUL -----------------------')





def Load_OTC():
    myname = current_thread().name  # Имя потока
    print('[%s] Started %s Load_OTC'%(time.ctime(), myname))

    # Очищаем таблицу
    # sql_truncate()

    #############################################################################################################
    # print(get_date('ОТС'))
    # Получаем дату загрузки
    lock.acquire()
    load_date = datetime.strptime(get_date('ОТС'), '%d.%m.%Y')
    lock.release()

    while load_date <= datetime.now():
        print(load_date)
        try:
            print('------- ОТС --------')
            # Парсим ОТС
            print('ОТС - Дата {n}'.format(n=str(load_date)))
            for s1 in otc.startparseOTC(load_date):  # Получаем список полей
                 number = s1[2]
                 if purchase_distinct(number) == True:
                    lock.acquire()  # Блокируем процесс для вставки в таблицу
                    sql_insert(s1)  # Вставляем поля в таблицу
                    print('OTC')
                    lock.release()  # Отпускаем блокировку
                    time.sleep(3)
                 else:
                     print('Закупка уже была загружена')
                     time.sleep(2)

        except BaseException as err:
            print(err)
            load_date = load_date + timedelta(days=1)

        load_date = load_date+timedelta(days=1)
    print('[%s] Completed %s Load_OTC'%(time.ctime(), myname))

def Load_SBER():
    myname = current_thread().name  # Имя потока
    print('[%s] Started %s Load_SBER'%(time.ctime(), myname))

    #############################################################################################################

    # Получаем дату загрузки
    lock.acquire()
    load_date = get_date('Сбербанк')
    lock.release()

    # настройка заголовков
    headers = {'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
               'X-Requested-With': 'XMLHttpRequest'
               }



    print('------- СБЕРБАНК --------')
    # Парсим сбербанк
    nextlist = True
    n = 0

    while nextlist == True:
        try:
           print('Сбербанк - Страница {n}'.format(n=str(n)))
           for s in sb.startparseSber(n, headers, load_date):  # Для каждой ссылки на странице
               # print(s)

                try:
                    number = sb.sberParser(s)[2]
                    if purchase_distinct(number) == True:
                        lock.acquire()  # Блокируем процесс для вставки в таблицу
                        sql_insert(sb.sberParser(s))  # Получаем список полей
                        print('SBER')
                        lock.release()  # Отпускаем блокировку
                        time.sleep(5)
                    else:
                        print ('Закупка уже была загружена')
                        time.sleep(2)
                except BaseException as e:
                    print(e)
                    continue

           n += 1

           time.sleep(5)
        except BaseException as err:
               print(err)
               break
    print('[%s] Completed %s Load_SBER'%(time.ctime(), myname))

def Load_ETP():
    myname = current_thread().name  # Имя потока
    print('[%s] Started %s Load_ETP'%(time.ctime(), myname))

    #############################################################################################################

    # Получаем дату загрузки
    lock.acquire()
    load_date = get_date('223ETP.ZAKAZRF')
    lock.release()

    print('------- ЕТП --------')
    # Парсим ЕТП
    nextlist = True
    for type in ['ZP', 'OK']:
        n = 0
        while nextlist == True:
             try:
                print('ЕТП - Страница {n}'.format(n=str(n)))
                for s in etp.startparseETP(n, type, load_date):  # Для каждой ссылке на странице
                    number = etp.etpParser(s)[2]
                    if purchase_distinct(number) == True:
                        lock.acquire()  # Блокируем процесс для вставки в таблицу
                        sql_insert(etp.etpParser(s))  # Получаем список полей и вставляем в таблицу
                        print('ETP')
                        lock.release()  # Отпускаем блокировку
                        time.sleep(3)
                    else:
                        print ('Закупка уже была загружена')
                        time.sleep(2)
                n += 1
                time.sleep(5)
             except BaseException as err:
                print(err)
                break
    print('[%s] Completed %s Load_ETP'%(time.ctime(), myname))


def Load_Rosel():
    myname = current_thread().name  # Имя потока
    print('[%s] Started %s Load_Rosel'%(time.ctime(), myname))

#############################################################################################################

    headers = {'Accept': "*/*",
               'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
               'X-Requested-With': 'XMLHttpRequest'
               }

    # Получаем дату загрузки
    lock.acquire()
    load_date = get_date('Россельторг')
    lock.release()

    print('------- РОСЭЛТОРГ --------')
    # Парсим РОСЭЛТОРГ
    nextlist = True
    n = 0
    while nextlist == True:
        try:
           print('РОСЭЛТОРГ - Страница {n}'.format(n=str(n)))
           for s1 in rs.startparseRoseltorg(n, headers, load_date):  # Получаем список полей
               number = s1[2]
               if purchase_distinct(number) == True:
                   lock.acquire()  # Блокируем процесс для вставки в таблицу
                   sql_insert(s1)  # Вставляем поля в таблицу
                   print('ROSEL')
                   lock.release()  # Отпускаем блокировку
                   time.sleep(3)
               else:
                   print('Закупка уже была загружена')
                   time.sleep(2)
           n += 1
           time.sleep(5)
        except BaseException as err:
            print (err)
            break

    print('[%s] Completed %s Load_Rosel'%(time.ctime(), myname))


if __name__ == '__main__':
    # Запускаем процессы
    Thread(target=Load_OTC).start()
    Thread(target=Load_SBER).start()
    Thread(target=Load_ETP).start()
    Thread(target=Load_Rosel).start()
