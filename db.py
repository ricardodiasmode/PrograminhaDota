import mysql.connector
from time import sleep

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="250491",
    port=3306,
    database="mydatabase"
)

cursor = mydb.cursor()

# TODO add IF Statement to when db doesn't exists

# cursor.execute("CREATE DATABASE mydatabase")


cursor.execute("DROP TABLE IF EXISTS hardsupp")
cursor.execute("DROP TABLE IF EXISTS softsupp")
cursor.execute("DROP TABLE IF EXISTS offlane")
cursor.execute("DROP TABLE IF EXISTS midlane")
cursor.execute("DROP TABLE IF EXISTS hardcarry")
cursor.execute("CREATE TABLE hardsupp (id INT AUTO_INCREMENT PRIMARY KEY, hero VARCHAR(255), coefficient VARCHAR(255))")
cursor.execute("CREATE TABLE softsupp (id INT AUTO_INCREMENT PRIMARY KEY, hero VARCHAR(255), coefficient VARCHAR(255))")
cursor.execute("CREATE TABLE offlane (id INT AUTO_INCREMENT PRIMARY KEY, hero VARCHAR(255), coefficient VARCHAR(255))")
cursor.execute("CREATE TABLE midlane (id INT AUTO_INCREMENT PRIMARY KEY, hero VARCHAR(255), coefficient VARCHAR(255))")
cursor.execute("CREATE TABLE hardcarry (id INT AUTO_INCREMENT PRIMARY KEY, hero VARCHAR(255), coefficient VARCHAR(255))")


def hardsuppDB():
    sql = "INSERT INTO hardsupp (hero, coefficient) VALUES (%s, %s)"
    file = open('HardSuppHeroes Victory Coefficient.txt', 'r')
    file_content = file.readlines()
    file.close()
    unparsed_values = [line.split() for line in file_content]

    x = 1
    while x < 25:
        for i in unparsed_values[x]:
            values = (unparsed_values[x][0], unparsed_values[x][-1])
            cursor.execute(sql, values)
            x += 1

def softsuppDB():
    sql = "INSERT INTO softsupp (hero, coefficient) VALUES (%s, %s)"
    file = open('SuppHeroes Victory Coefficient.txt', 'r')
    file_content = file.readlines()
    file.close()
    unparsed_values = [line.split() for line in file_content]

    x = 1
    while x < 25:
        for i in unparsed_values[x]:
            values = (unparsed_values[x][0], unparsed_values[x][-1])
            cursor.execute(sql, values)
            x += 1


def offlaneDB():
    sql = "INSERT INTO offlane (hero, coefficient) VALUES (%s, %s)"
    file = open('OfflanerHeroes Victory Coefficient.txt', 'r')
    file_content = file.readlines()
    file.close()
    unparsed_values = [line.split() for line in file_content]

    x = 1
    while x < 25:
        for i in unparsed_values[x]:
            values = (unparsed_values[x][0], unparsed_values[x][-1])
            cursor.execute(sql, values)
            x += 1


def midlaneDB():
    sql = "INSERT INTO midlane (hero, coefficient) VALUES (%s, %s)"
    file = open('MidlanerHeroes Victory Coefficient.txt', 'r')
    file_content = file.readlines()
    file.close()
    unparsed_values = [line.split() for line in file_content]

    x = 1
    while x < 25:
        for i in unparsed_values[x]:
            values = (unparsed_values[x][0], unparsed_values[x][-1])
            cursor.execute(sql, values)
            x += 1


def hardcarryDB():
    sql = "INSERT INTO hardcarry (hero, coefficient) VALUES (%s, %s)"
    file = open('HCHeroes Victory Coefficient.txt', 'r')
    file_content = file.readlines()
    file.close()
    unparsed_values = [line.split() for line in file_content]

    x = 1
    while x < 25:
        for i in unparsed_values[x]:
            values = (unparsed_values[x][0], unparsed_values[x][-1])
            cursor.execute(sql, values)
            x += 1


hardsuppDB()
softsuppDB()
offlaneDB()
midlaneDB()
hardcarryDB()
mydb.commit()

