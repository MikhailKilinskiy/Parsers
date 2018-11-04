
import pyodbc
from datetime import timedelta, datetime
import modules.otc as otc
import pyodbc

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
        SQLCommand = (
        "SELECT PurchaseNumber FROM [OOS_DWH].[dbo223].[ContractGuaranteeParser] WHERE PurchaseNumber = ?")
        Values = number
        cursor.execute(SQLCommand, Values)
        data = cursor.fetchall()

        if len(data) == 0:
            return True
        else:
            return False

if __name__ == '__main__':

    print('------- ОТС --------')
    # Парсим РОСЭЛТОРГ
    nextlist = True
    n = 0
    while nextlist == True:
        try:
            print('РОСЭЛТОРГ - Страница {n}'.format(n=str(n)))
            for s1 in otc.startparseOTC(n, ):  # Получаем список полей
                number = s1[2]
                if purchase_distinct(number) == True:
                    sql_insert(s1)  # Вставляем поля в таблицу
                    time.sleep(3)
                else:
                    print('Закупка уже была загружена')
                    time.sleep(2)
            n += 1
            time.sleep(5)
        except BaseException as err:
            print(err)
            break
