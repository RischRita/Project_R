import mysql.connector
from mysql.connector import Error
from local_settings2 import HOST, USER, PASSWORD, DATABASE
from sql_queries import log_search_term, search_movies, search_movies_by_genre, search_movies_by_year, get_genres, get_keyWords
from menu import show_menu

def connect_to_db(host, user, password, database):
    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def display_films(films):
    """Функция для отображения списка фильмов с навигацией по страницам"""
    num_films = len(films)
    if num_films == 0:
        print("По вашему запросу ничего не найдено.")
        return

    page_size = 10
    current_page = 0
    page_count = (num_films + page_size - 1) // page_size

    while True:
        start_index = current_page * page_size
        end_index = min(start_index + page_size, num_films)

        print(f"\nСтраница {current_page + 1} из {page_count}\n")
        films_to_show = films[start_index:end_index]

        for i, film in enumerate(films_to_show, start=1):
            print(f"{start_index + i}. Название: {film[0]}")
            print(f"   Описание: {film[1]}")
            print(f"   Год выпуска: {film[2]}")
            print("-" * 50)

        if page_count > 1:
            next_page = input("\nВведите 2 для следующей страницы, 1 для предыдущей, 0 для выхода: ")
            if next_page == "2" and current_page < page_count - 1:
                current_page += 1
            elif next_page == "1" and current_page > 0:
                current_page -= 1
            elif next_page == "0":
                break
            else:
                print("\nНекорректная команда или такой страницы не существует.")
        else:
            break

def main():
    print("Добро пожаловать в систему поиска фильмов!")

    with connect_to_db(HOST, USER, PASSWORD, DATABASE) as connection, connection.cursor() as cursor:
        while True:
            show_menu()
            choice = input("Выберите пункт меню: ")

            if choice == "1":
                print("Запрос по ключевому слову")
                keyWord = input("Введите ключевое слово: ")
                films = search_movies(cursor, keyWord)
                log_search_term(cursor, keyWord)
                connection.commit()
                print(f"Найдено фильмов: {len(films)}")
                display_films(films)

            elif choice == "2":
                print("Запрос по жанру")
                genres = get_genres(cursor)
                print("Доступные жанры:")
                for idx, genre in enumerate(genres, 1):
                    print(f"{idx}. {genre}")

                genre_choice = int(input("Выберите номер жанра: "))
                selected_genre = genres[genre_choice - 1]
                films = search_movies_by_genre(cursor, selected_genre)
                print(f"Найдено фильмов: {len(films)}")
                display_films(films)

            elif choice == "3":
                print("Запрос по году")
                year1 = int(input("Введите начальный год: "))
                year2 = int(input("Введите конечный год: "))
                films = search_movies_by_year(cursor, year1, year2)
                print(f"Найдено фильмов: {len(films)}")
                display_films(films)

            elif choice == "4":
                print("Вывод популярных запросов")
                result = get_keyWords(cursor)
                num_requests = len(result)
                print(f"Найдено популярных запросов: {num_requests}")

                if num_requests == 0:
                    print("Популярные запросы не найдены.")
                else:
                    page_size = 10
                    current_page = 0
                    page_count = (num_requests + page_size - 1) // page_size

                    while True:
                        start_index = current_page * page_size
                        end_index = min(start_index + page_size, num_requests)

                        print(f"\nСтраница {current_page + 1} из {page_count}\n")
                        requests_to_show = result[start_index:end_index]

                        for i, keyWord in enumerate(requests_to_show, start=1):
                            print(f"{start_index + i}. Популярный запрос: {keyWord[0]}, Количество: {keyWord[1]}")
                            print("-" * 50)

                        if page_count > 1:
                            next_page = input("\nВведите 2 для следующей страницы, 1 для предыдущей, 0 для выхода: ")
                            if next_page == "2" and current_page < page_count - 1:
                                current_page += 1
                            elif next_page == "1" and current_page > 0:
                                current_page -= 1
                            elif next_page == "0":
                                break
                            else:
                                print("\nНекорректная команда или такой страницы не существует.")
                        else:
                            break

            elif choice == "5":
                print("Выход из программы")
                break

            else:
                print("Некорректный выбор. Попробуйте снова.")



if __name__ == "__main__":
    main()
