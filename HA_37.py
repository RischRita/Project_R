#1. В базе данных ich_edit три таблицы. Users с полями (id, name, age), Products с полями
# (pid, prod, quantity) и Sales с полями (sid, id, pid).

#Программа должна запросить у пользователя название таблицы и вывести все ее строки или
# сообщение, что такой таблицы нет.


import mysql.connector
from local_settings import HOST, USER, PASSWORD, DATABASE


dbconfig = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'database': DATABASE,
}


connection = mysql.connector.connect(**dbconfig)
cursor = connection.cursor()


cursor.execute("SHOW TABLES")
tables = cursor.fetchall()


print("Список таблиц в базе данных:")
for table in tables:
    print(table[0])


table_name = input("Введите название таблицы для отображения данных: ")


if (table_name,) in tables:

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    print(f" ===== Table '{table_name}': =====")
    for row in rows:
        print(row)
else:
    print(f"Таблицы с названием '{table_name}' нет в базе данных.")


cursor.close()
connection.close()

import mysql.connector

# Конфигурация подключения
dbconfig = {
    'host': 'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
    'user': 'ich1',
    'password': 'password',
    'database': 'ich_edit'
}

try:
    # Установка соединения с базой данных
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor()

    # Запрос всех уникальных имен пользователей
    cursor.execute("SELECT DISTINCT name FROM Users")
    result = cursor.fetchall()
    names = [res[0] for res in result]

    # Печать списка пользователей
    print("В таблице Users есть пользователи:")
    print(*names, sep=", ")

    # Ввод имени пользователя
    name = input("Выберите одного из них: ").strip()

    if name not in names:
        print("Такого пользователя нет.")
    else:
        # Запрос покупок выбранного пользователя
        query = """
        SELECT u.name, u.age, p.prod
        FROM Users u
        JOIN Sales s ON u.id = s.id
        JOIN Products p ON p.pid = s.pid
        WHERE u.name = %s
        """
        cursor.execute(query, (name,))
        result = cursor.fetchall()

        if not result:
            print(f"У пользователя {name} нет покупок.")
        else:
            # Печать результатов
            print("ИМЯ\t\tВОЗРАСТ\t\tТОВАР")
            for row in result:
                print(*row, sep="\t\t")

except mysql.connector.Error as err:
    print(f"Ошибка подключения к базе данных: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Подключение закрыто.")
