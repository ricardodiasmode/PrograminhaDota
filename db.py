import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="leandro",
    password="250491",
    database="mydatabase"
)

cursor = mydb.cursor()

# TODO add IF Statement to when db doesn't exists

# cursor.execute("CREATE DATABASE mydatabase")
cursor.execute("CREATE TABLE hardsupp (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
cursor.execute("CREATE TABLE softsupp (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
cursor.execute("CREATE TABLE offlane (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
cursor.execute("CREATE TABLE midlane (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
cursor.execute("CREATE TABLE hardcarry (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")


def hardsuppDB():
    sql = f"INSERT INTO hardsupp (hero, coefficient) VALUES (%s, %s)"
    file = open('HardSuppHeroes Victory Coefficient.txt', 'r')
    file_content = file.readlines()
    file.close()
    unparsed_values = [line.split() for line in file_content]

    x = 1
    while x < 25:
        for i in unparsed_values[x]:
            values = (unparsed_values[x][1], unparsed_values[x][-1])
            x += 1
            cursor.executemany(sql, values)


def softsuppDB():
    sql = f"INSERT INTO softsupp (hero, coefficient) VALUES (%s, %s)"
    file = open('SuppHeroes Victory Coefficient.txt', 'r')
    file_content = file.readlines()
    file.close()
    unparsed_values = [line.split() for line in file_content]

    x = 1
    while x < 25:
        for i in unparsed_values[x]:
            values = (unparsed_values[x][1], unparsed_values[x][-1])
            x += 1
            cursor.executemany(sql, values)


def offlaneDB():
    sql = f"INSERT INTO offlane (hero, coefficient) VALUES (%s, %s)"
    file = open('OfflanerHeroes Victory Coefficient.txt', 'r')
    file_content = file.readlines()
    file.close()
    unparsed_values = [line.split() for line in file_content]

    x = 1
    while x < 25:
        for i in unparsed_values[x]:
            values = (unparsed_values[x][1], unparsed_values[x][-1])
            x += 1
            cursor.executemany(sql, values)


def midlaneDB():
    sql = f"INSERT INTO midlane (hero, coefficient) VALUES (%s, %s)"
    file = open('MidlanerHeroes Victory Coefficient.txt', 'r')
    file_content = file.readlines()
    file.close()
    unparsed_values = [line.split() for line in file_content]

    x = 1
    while x < 25:
        for i in unparsed_values[x]:
            values = (unparsed_values[x][1], unparsed_values[x][-1])
            x += 1
            cursor.executemany(sql, values)


def hardcarryDB():
    sql = f"INSERT INTO hardcarry (hero, coefficient) VALUES (%s, %s)"
    file = open('HCHeroes Victory Coefficient.txt', 'r')
    file_content = file.readlines()
    file.close()
    unparsed_values = [line.split() for line in file_content]

    x = 1
    while x < 25:
        for i in unparsed_values[x]:
            values = (unparsed_values[x][1], unparsed_values[x][-1])
            x += 1
            cursor.executemany(sql, values)


hardsuppDB()
softsuppDB()
offlaneDB()
midlaneDB()
hardcarryDB()
