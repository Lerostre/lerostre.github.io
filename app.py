from flask import Flask, render_template, request
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from logging import FileHandler, WARNING
from flask import Response
from flask import send_file
from flask import redirect, url_for
import numpy as np
import csv
import random

webapp = Flask(__name__)

webapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
webapp.config['SQLALCHEMY_ECHO'] = True
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
db = SQLAlchemy(webapp)

@webapp.route('/')
def index():
    return render_template("webindex.html")

@webapp.route('/', methods=['POST'])
def my_form_post():
    ingr = request.form['text']
    if ingr:
        list_recipe = []
        with open('static/ingredients_from_eda.ru.csv', encoding='utf-8') as r_file:
            data_reader = csv.DictReader(r_file)
            for line in data_reader:
                if ingr == line['ingredient']:
                    list_recipe.append(line['name'])
        print(np.random.choice(list_recipe))
        return render_template('webindex.html', result=np.random.choice(list_recipe))

def get_rand(ingr):
    list_recipe = []
    with open('static/ingredients_from_eda.ru.csv', encoding='utf-8') as r_file:
        data_reader = csv.DictReader(r_file)
        for line in data_reader:
            if ingr == line['ingredient']:
                list_recipe.append(line['name'])
    return random.shuffle(list_recipe)

if __name__ == '__main__':
    # остатки от попыток перехода в постгрес, пока работает - не трогаю
    webapp.jinja_env.auto_reload = True
    webapp.config['TEMPLATES_AUTO_RELOAD'] = True
    webapp.run(host="0.0.0.0", port=5000, debug=True)
