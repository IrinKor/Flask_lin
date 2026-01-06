# -*- coding: UTF-8 -*-
import os

from flask import Flask, g, render_template, request, jsonify, url_for, send_file, redirect

import lego_data
import datetime
import settings

from models import Set, db_session,Parts

app = Flask(__name__, template_folder="templates")

app.config['SECRET_KEY'] = settings.SECRET_KEY
EMPL = [
    {"имя": "Дмитрий", "фамилия": "Иванов", "должность": "Разработчик", "руководитель": False, "дата_рождения": "1990-06-15", "kpi": 85, "пол": True},
    {"имя": "Екатерина", "фамилия": "Смирнова", "должность": "Менеджер", "руководитель": True, "дата_рождения": "1985-03-22", "kpi": 92, "пол": False},
    {"имя": "Игорь", "фамилия": "Петров", "должность": "Аналитик", "руководитель": False, "дата_рождения": "1992-11-10", "kpi": 78, "пол": True},
    {"имя": "Оксана", "фамилия": "Козлова", "должность": "HR", "руководитель": True, "дата_рождения": "1988-09-05", "kpi": 88, "пол": False},
    {"имя": "Владислав", "фамилия": "Сидоров", "должность": "Тестировщик", "руководитель": False, "дата_рождения": "1995-07-30", "kpi": 80, "пол": True},
    {"имя": "Анна", "фамилия": "Морозова", "должность": "Маркетолог", "руководитель": False, "дата_рождения": "1993-12-12", "kpi": 89, "пол": False},
    {"имя": "Сергей", "фамилия": "Волков", "должность": "DevOps", "руководитель": False, "дата_рождения": "1987-08-25", "kpi": 90, "пол": True},
    {"имя": "Мария", "фамилия": "Федорова", "должность": "Дизайнер", "руководитель": False, "дата_рождения": "1994-04-18", "kpi": 84, "пол": False},
    {"имя": "Алексей", "фамилия": "Зайцев", "должность": "Разработчик", "руководитель": True, "дата_рождения": "1983-05-20", "kpi": 95, "пол": True},
    {"имя": "Юлия", "фамилия": "Тихонова", "должность": "Финансист", "руководитель": True, "дата_рождения": "1986-10-03", "kpi": 91, "пол": False},
]

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.htm'), 404

@app.route("/")
def index():
    return render_template('main.htm', EMPL=EMPL)

@app.route("/news/<int:year>/<int:month>/<int:day>/<path:my_url>")
def news_by_date(year, month, day, my_url):
    return f'News by {year} year etc ({my_url})'

@app.route("/sets/<int:page>")
def catalog(page):
    items, pages = Set.load_limited(page)
    return render_template('sets.htm', items=items, page=page, pages=pages)

@app.route("/details/<int:page>")
def catalogDit(page):
    items, pages = Parts.load_limited(page)
    return render_template('details.htm', items=items, page=page, pages=pages)

@app.route("/search/")
def search():
    query = request.form.get("query", "")
    items = Set.search_by_name(query)
    return render_template('sets.htm', items=items, page=0, pages=0)


##@app.route("/<page_name>/")
##def main(page_name):
##    return render_template(page_name+'.htm')


if __name__ == "__main__":
##    #Еще один способ добавления статической дирректории
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })
    app.run(host='0.0.0.0', port=5050, debug=True)
