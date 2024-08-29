import mysql.connector
from local_settings import (HOST,USER,PASSWORD,DATABASE)
def connect_to_db(host, user, password, database):
    return mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database

    )


def search_movies_by_year(year1,year2):
    connection = connect_to_db(HOST,USER,PASSWORD,DATABASE)
    cursor = connection.cursor()
    query = "SELECT title,description,release_year FROM sakila.film WHERE release_year BETWEEN %s AND %s"
    cursor.execute(query, (year1,year2))
    result = cursor.fetchall()
    return result


def search_movies(keyWord):
    connection = connect_to_db(HOST,USER,PASSWORD,DATABASE)
    cursor = connection.cursor()
    query = "SELECT title,description,release_year FROM sakila.film WHERE title LIKE %s OR description LIKE %s"
    cursor.execute(query, (f"%{keyWord}%", f"%{keyWord}%"))
    #cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return  result


from Project_Risch.menu import show_menu


def main():
    print("Добро пожаловать в систему поиска фильмов!")
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ")


        if choice == "1":
            print("Запрос по ключевому слову")
            # Вызов функции обработки поиска по ключевому слову
            keyWord = input("Введите ключевое слово: ")
            films = search_movies(keyWord)
            if films:
                for film in films:
                    print (f"Название: {film[0]}, Описание: {film[1]}, Год: {film[2]}")
                    print("-")
            else:
                print("По Вашему запросу ничего  не найдено")
        elif choice == "2":
            print("Запрос по жанру")
            # Вызов функции обработки поиска по жанру
        elif choice == "3":
            print("Запрос по году")
            # Вызов функции обработки поиска по году
            year1 = int( input("Введите год"))
            year2 = int( input("Введите год"))
            films = search_movies_by_year(year1,year2)
            if films:
                for film in films:
                    print (f"Название: {film[0]}, Описание: {film[1]}, Год: {film[2]}")
                    print("-")
            else:
                print("По Вашему запросу ничего  не найдено")



        elif choice == "4":
            print("Вывод популярных запросов")
            # Вызов функции для отображения популярных запросов
        elif choice == "0":
            print("Выход из программы")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
