import sqlite3
import config


def connect_db(sql_request, *args):
    """
    Подключение к БД и выполнение запроса с заданными аргументами
    :param sql_request:
    :param args:
    :return:
    """
    with sqlite3.connect(config.NAME_DB) as connect:
        cursor = connect.cursor()
        cursor.execute(sql_request, args)
        return cursor.fetchall()


def name_of_film(name):
    """
    Получение информации о фильме по его названию
    :param name:
    :return:
    """
    sql_request = """
                    SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE title = (@name)
                    ORDER BY release_year LIMIT 1
                    """
    query = connect_db(sql_request, name)
    result = {'title': query[0][0],
              'country': query[0][1],
              'release_year': query[0][2],
              'genre': query[0][3],
              'description': query[0][4]}
    return result


def year_to_year(first_year, second_year):
    """
    Получение списка фильмов за период указанный в запросе
    :param first_year:
    :param second_year:
    :return:
    """
    sql_request = """
                    SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN (@first_year) AND (@second_year)
                    ORDER BY release_year DESC LIMIT 100
                    """
    query = connect_db(sql_request, first_year, second_year)
    result = []
    for item in query:
        result.append({'title': item[0], 'release_year': item[1]})
    return result


def rating_film(film_list):
    """
    Формирование конечного списка фильмов по возрастным рейтингам
    :param film_list:
    :return:
    """
    result = []
    for item in film_list:
        result.append({'title': item[0], 'rating': item[1], 'description': item[2]})
    return result


def children_films():
    """
    Получение списка фильмов для детей (возрастной рейтинг G)
    :return:
    """
    sql_request = """
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ("G")
                    ORDER BY title
                    """
    query = connect_db(sql_request)
    result = rating_film(query)
    return result


def family_films():
    """
    Получение списка фильмов для всей семьи (возрастной рейтинг G, PG, PG-13)
    :return:
    """
    sql_request = """
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ("G", "PG", "PG-13")
                    ORDER BY title
                    """
    query = connect_db(sql_request)
    result = rating_film(query)
    return result


def adult_films():
    """
    Получение списка фильмов не для детей (возрастной рейтинг R, NC-17)
    :return:
    """
    sql_request = """
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ("R", "NC-17")
                    ORDER BY title
                    """
    query = connect_db(sql_request)
    result = rating_film(query)
    return result


def genre_of_film(genre):
    """
    Получение списка фильмов по жанру
    :param genre:
    :return:
    """
    genre = f"%{genre}%"
    sql_request = """
                    SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE @genre
                    ORDER BY title
                    """
    query = connect_db(sql_request, genre)
    result = []
    for item in query:
        result.append({'title': item[0], 'description': item[1]})
    return result


def get_result_list_actor(query):
    """
    Обработка и формирование конечного списка актеров для функции get_actor
    :param query:
    :return:
    """
    result_actor_list = {}
    for item in query:
        for actors in item:
            actor_list = actors.split(", ")
            for actor in actor_list:
                try:
                    result_actor_list[actor] += 1
                except KeyError:
                    result_actor_list[actor] = 1
    result = []
    for key, value in result_actor_list.items():
        if value > 2:
            result.append(key)
    return result


def get_actor(first_actor, second_actor):
    """
    Получение списка актеров сыгравших более 2 раз с заданными актерами
    :param first_actor:
    :param second_actor:
    :return:
    """
    f_actor = f"%{first_actor}%"
    s_actor = f"%{second_actor}%"
    sql_request = """
                    SELECT "cast"
                    FROM netflix
                    WHERE "cast" LIKE @f_actor
                    AND "cast" LIKE @s_actor
                    
                    """
    query = connect_db(sql_request, f_actor, s_actor)
    result = get_result_list_actor(query)
    result.remove(first_actor)
    result.remove(second_actor)
    return result


def list_of_films(film_type, year, genre):
    """
    Получение спика фильмов по заданному типу, году выпуска и жанру
    :param film_type:
    :param year:
    :param genre:
    :return:
    """
    genre = f"%{genre}%"
    film_type = f"%{film_type}%"
    sql_request = """
                    SELECT title, description
                    FROM netflix
                    WHERE "type" LIKE @film_type
                    AND release_year = (@year)
                    AND listed_in LIKE @genre
                    ORDER BY title
                    """
    query = connect_db(sql_request, film_type, year, genre)
    result = []
    for item in query:
        result.append({'title': item[0], 'description': item[1]})
    return result
