from flask import Blueprint, redirect, jsonify
import utils

main_blueprint = Blueprint("main_blueprint", __name__)


@main_blueprint.route("/")
def main_page():
    """
    Функция перенаправления с главной страницы сервера, т.к. главная страница в проекте не задействована
    :return:
    """
    return redirect("http://127.0.0.1:5000/movie/2 States", code=302)


@main_blueprint.route("/movie/<title>")
def film_name_page(title):
    """
    Обработка запроса по названию фильма
    :param title:
    :return:
    """
    film_name = utils.name_of_film(title)
    return jsonify(film_name)


@main_blueprint.route("/movie/<f_year>/to/<s_year>")
def film_year_page(f_year, s_year):
    """
    Обработка запроса по периоду выхода фильмов
    :param f_year:
    :param s_year:
    :return:
    """
    film_years = utils.year_to_year(f_year, s_year)
    return jsonify(film_years)


@main_blueprint.route("/rating/<rating>")
def rating_film(rating):
    """
    Обработка запроса по возратному рейтингу (детский, для всей семьи, взрослый)
    :param rating:
    :return:
    """
    if rating == "children":
        film_rating = utils.children_films()
    if rating == "family":
        film_rating = utils.family_films()
    if rating == "adult":
        film_rating = utils.adult_films()
    return jsonify(film_rating)


@main_blueprint.route("/genre/<type_genre>")
def family_film(type_genre):
    """
    Обработка запроса по жанру фильмов
    :param type_genre:
    :return:
    """
    genre_films = utils.genre_of_film(type_genre)
    return jsonify(genre_films)


@main_blueprint.route("/actor/<first_actor>/<second_actor>")
def get_actor(first_actor, second_actor):
    """
    Обработка запроса по поиску актеров игравших более 2-х раз с искомыми актерами
    :return:
    """
    actors = utils.get_actor(first_actor, second_actor)
    return jsonify(actors)


@main_blueprint.route("/list/<film_type>/<int:year>/<genre>")
def list_of_films(film_type, year, genre):
    """
    Обработка запроса поска фильма по типу, году выпуска и жанру
    :param film_type:
    :param year:
    :param genre:
    :return:
    """
    films = utils.list_of_films(film_type, year, genre)
    return films

