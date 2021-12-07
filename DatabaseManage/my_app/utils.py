import sys
import pymysql
from my_app.models import Users, Datatype
from my_app import db, app
from flask_login import current_user
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import requests


def add_user(email, username, password):
    user = Users(FullName='', UserName=username, Password=password, Email=email, Phone='', IsAdmin=0, Active=1,
                 Avatar='')
    db.session.add(user)
    try:
        db.session.commit()
        return True
    except:
        return False


def get_all_database(username):
    rds_host = "dbtest.cctxaxqlrtny.us-east-1.rds.amazonaws.com"
    name = "admin"
    password = "quang810"
    db_name = ""

    data = ()

    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(e)
        sys.exit()

    try:
        with conn.cursor() as cur:
            query = "SHOW DATABASES"
            cur.execute(query)
            data = cur.fetchall()
        conn.commit()
    except Exception as e:
        print(e)
    databaseOfUser = []
    countDatabase = 0
    for item in data:
        getNameDatabase = '({})'.format(item)
        check = getNameDatabase.find(username)
        if check != -1:
            database = ""
            for i in getNameDatabase:
                if i == "(" or i == ")" or i == "'" or i == ",":
                    continue
                else:
                    database += i
            newNameDatabase = database.replace(username + '_', '')
            countDatabase += 1
            databaseOfUser.append(newNameDatabase)
    return databaseOfUser


def get_all_datatype():
    datatype = Datatype.query.all()
    return datatype


def get_all_table_of_database(userName):
    rds_host = "dbtest.cctxaxqlrtny.us-east-1.rds.amazonaws.com"
    name = "admin"
    password = "quang810"
    db_name = ""

    data = ()

    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(e)
        sys.exit()

    try:
        with conn.cursor() as cur:
            query = "SHOW TABLES FROM " + userName
            cur.execute(query)
            data = cur.fetchall()
        conn.commit()
    except Exception as e:
        print(e)
    convertData = ConvertNameTableDatabase(data)
    return convertData


def ConvertNameTableDatabase(data):
    newData = []
    for item in data:
        convertItem = str(item)
        newItem = ""
        for value in convertItem:
            if value == "(" or value == ")" or value == "'" or value == ",":
                continue
            else:
                newItem += value
        newData.append(newItem)
    return newData


def GetDatabase(data):
    newData = ""
    for i in range(len(data)):
        if data[i] == "?":
            for j in range(i):
                newData += data[j]
            return newData
    return newData


def GetTable(data):
    newData = ""
    for i in range(len(data)):
        if data[i] == "=":
            i = i + 1
            for j in range(i, len(data)):
                newData += data[j]
            return newData
    return newData


def GetAllColumnOfTable(namedatabase, nametable):
    rds_host = "dbtest.cctxaxqlrtny.us-east-1.rds.amazonaws.com"
    name = "admin"
    password = "quang810"
    db_name = ""

    data = []

    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(e)
        sys.exit()

    try:
        with conn.cursor() as cur:
            query = "SHOW COLUMNS FROM " + namedatabase + "." + nametable
            cur.execute(query)
            data = cur.fetchall()
        conn.commit()
    except Exception as e:
        print(e)

    newData = []
    for item in data:
        newData.append(item[0])
    return newData


def GetAllInfoTable(namedatabase, nametable):
    rds_host = "dbtest.cctxaxqlrtny.us-east-1.rds.amazonaws.com"
    name = "admin"
    password = "quang810"
    db_name = ""

    data = []

    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(e)
        sys.exit()

    try:
        with conn.cursor() as cur:
            query = "SHOW COLUMNS FROM " + namedatabase + "." + nametable
            cur.execute(query)
            data = cur.fetchall()
        conn.commit()
    except Exception as e:
        print(e)

    return data


def GetAllDataOfTableInDatabase(namedatabase, nametable):
    rds_host = "dbtest.cctxaxqlrtny.us-east-1.rds.amazonaws.com"
    name = "admin"
    password = "quang810"
    db_name = ""

    data = []

    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(e)
        sys.exit()

    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM " + namedatabase + "." + nametable
            cur.execute(query)
            data = cur.fetchall()
        conn.commit()
    except Exception as e:
        print(e)
    return data


def GetUrlEditTable(data):
    listUrl = []
    size = 0
    for item in data:
        size = len(item)
        url = ""
        for i in range(size):
            url += ("?" + str(item[i]))
        listUrl.append(url)

    return listUrl


def CountRowTable(namedatabase, nametable):
    rds_host = "dbtest.cctxaxqlrtny.us-east-1.rds.amazonaws.com"
    name = "admin"
    password = "quang810"
    db_name = ""

    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(e)
        sys.exit()

    try:
        with conn.cursor() as cur:
            query = "SELECT COUNT(*) FROM " + namedatabase + "." + nametable
            cur.execute(query)
            data = cur.fetchall()
        conn.commit()
    except Exception as e:
        print(e)
    return data


def UpdateInfoAddRowDatabase(namedatabase, nametable):
    rds_host = "dbtest.cctxaxqlrtny.us-east-1.rds.amazonaws.com"
    name = "admin"
    password = "quang810"
    db_name = ""

    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(e)
        sys.exit()
    try:
        with conn.cursor() as cur:
            query = "UPDATE ManageUser.InfoAddRowDatabase SET NameDatabase = '" + namedatabase + "', NameTable = '" + nametable + "' WHERE Id = 1"
            cur.execute(query)
        conn.commit()
    except Exception as e:
        print(e)


def GetInfoAddRowDatabase():
    rds_host = "dbtest.cctxaxqlrtny.us-east-1.rds.amazonaws.com"
    name = "admin"
    password = "quang810"
    db_name = ""

    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print(e)
        sys.exit()

    data = []
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM ManageUser.InfoAddRowDatabase"
            cur.execute(query)
            data = cur.fetchall()
        conn.commit()
    except Exception as e:
        print(e)

    outData = []
    nameDatabase = ""
    nameTable = ""
    for item in data:
        strData = str(item)
        str1 = strData.replace("(1, '", "")
        str2 = str1.replace("')", "")
        str3 = str2.replace("', '", "|")
        center = str3.find("|")
        for index in range(len(str3)):
            if index == center:
                continue
            elif index < center:
                nameDatabase += str3[index]
            else:
                nameTable += str3[index]
    outData.append(nameDatabase)
    outData.append(nameTable)
    return outData


def CheckChar(name, nameCheck):
    return name.find(nameCheck)


def SubmitAddTable(data):
    url = "https://sqs.us-east-1.amazonaws.com/126581837666/QueueAddDataTable"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    for item in data:
        payload = {
            "query": item,
        }
        payload = quote(str(payload))
        params = {
            'Action': 'SendMessage',
            'MessageBody': payload
        }
        send = requests.post(url, headers=headers, params=params)


def name(data):
    data = (data[data.find("?") + 1:len(data) - 1])
    start = data.find("name")
    end = data.find("table")
    data = data[start + 5:end - 3]
    return data


def table(data):
    data = (data[data.find("%3") + 3:len(data) - 1])
    start = data.find("table")
    end = data.find("info")
    data = data[start + 6:end - 3]
    return data


def info(data, option):
    if option == 1:
        data = (data[data.find("info") + 8:len(data) - 8])
    else:
        data = (data[data.find("info") + 8:len(data) - 9])
    return data.split("%3F")


def StringHandling(data, option):
    listData = [name(data), table(data)]
    listData.extend(info(data, option))
    return listData


def ConverUrl(data):
    value = ""
    for item in range(len(data)):
        if item == 0:
            value += "name=" + str(data[item])
        elif item == 1:
            value += "?table=" + str(data[item])
        elif item == 2:
            value += "?info=?" + str(data[item])
        else:
            value += "?" + str(data[item])
    return value


def CovertUpdateDataTable(listA, listB, option):
    string = ""
    for item in listA:
        string1 = item + ' = ' + "'" + listB[listA.index(item)] + "'"
        if listA.index(item) < len(listA) - 1:
            if option == 0:
                string1 = string1 + ', '
            else:
                string1 = string1 + ' AND '
        string = string + string1
    return string


def OuputQueryUpdateDataTable(list1, list2, list3, option):
    wherelist = list2[2:len(list2)]
    query = ""
    if option == 1:
        query = 'UPDATE ' + '.'.join([list2[0], list2[1]]) + ' SET ' + CovertUpdateDataTable(list1, list3,0) + \
            ' WHERE ' + CovertUpdateDataTable(list1, wherelist, 1)
    else:
        query = 'DELETE FROM ' + list2[0] + '.' + list2[1] + ' WHERE ' + CovertUpdateDataTable(list1, wherelist, 1)
    return query

def SendRequest(url, value):
    url = url
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "query": value,
    }
    payload = quote(str(payload))
    params = {
        'Action': 'SendMessage',
        'MessageBody': payload
    }
    send = requests.post(url, headers=headers, params=params)
