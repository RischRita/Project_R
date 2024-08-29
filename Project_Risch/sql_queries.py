# sql_queries.py

def log_search_term(cursor, search_term):
    cursor.execute("INSERT INTO keyWords (keyWord) VALUES (%s)", (search_term,))
    print(1)


def search_movies(cursor, keyWord, limit=10):
    query = """
    SELECT title, description, release_year 
    FROM film 
    WHERE title LIKE %s OR description LIKE %s
    LIMIT %s
    """
    cursor.execute(query, (f"%{keyWord}%", f"%{keyWord}%", limit))
    return cursor.fetchall()


def search_movies_by_genre(cursor, genre, limit=10):
    query = f"""
    SELECT f.title, f.description, f.release_year 
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s
    LIMIT %s
    """
    cursor.execute(query, (genre, limit))  # Передаем limit как параметр запроса
    return cursor.fetchall()


def search_movies_by_year(cursor, year1, year2, limit=10):
    query = """
    SELECT title, description, release_year 
    FROM film 
    WHERE release_year BETWEEN %s AND %s
    
    """
    cursor.execute(query, (year1, year2))
    return cursor.fetchall()

# sql_queries.py

def get_genres(cursor):
    query = "SELECT name FROM category"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def search_movies_by_genre(cursor, genre):
    query = """
    SELECT f.title, f.description, f.release_year 
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s
    """
    cursor.execute(query, (genre,))
    return cursor.fetchall()


def get_keyWords(cursor, limit=10):
    query = """
    SELECT keyWord,COUNT(*) AS keyword_count
    FROM keyWords
    GROUP BY keyWord
    ORDER BY keyword_count DESC
    LIMIT %s
    """
    cursor.execute(query, (limit,))
    return cursor.fetchall()