from flask import Flask, render_template, request
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from logging import FileHandler,WARNING
from flask import Response
from flask import send_file
from flask import redirect, url_for
import os
from config import DEV_DB

# docker.exe run -p 5000:5000 -e DEBUG=1 flask-site
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DEV_DB

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html")

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    language = db.Column(db.Text)
    age = db.Column(db.Integer)

    


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)

    def __repr__(self):
         return f"{self.id}, {self.q1}, {self.q2}, {self.q3}, {self.q4}, {self.q5}, {self.q6}"

@app.route('/questions')
def question_page():
    questions = Questions.query.all()
    return render_template(
        'questions.html',
        questions=questions
    )

@app.route('/questions1')
def question_page1():
    questions = Questions.query.all()
    return render_template(
        'questions1.html',
        questions=questions
    )

@app.route('/')
def home_page():
    return render_template(
        'index.html')

@app.route('/process', methods=['get'])
def answer_process():
    # если нет ответов, то отсылаем решать анкету
    if not request.args:
        return redirect(url_for('question_page'))
    
    # достаем параметры
    gender = request.args.get('gender')
    education = request.args.get('education')
    language = request.args.get('language')
    age = request.args.get('age')
    
    # создаем профиль пользователя
    user = User(
        age=age,
        gender=gender,
        education=education,
        language=language
    )
    
    # добавляем в базу
    db.session.add(user)
    # сохраняемся
    db.session.commit()

    #app.logger.info(user.id)

    # получаем юзера с айди (автоинкремент)
    db.session.refresh(user)
    
    # получаем два ответа
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')
    q6 = request.args.get('q6')
    
    # привязываем к пользователю (см. модели в проекте)
    answer = Answers(id=user.id, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6)
    # добавляем ответ в базу
    db.session.add(answer)
    # сохраняемся
    db.session.commit()
    return render_template('thanks.html')


@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = User.query.count()
    qs = [Answers.q1, Answers.q2, Answers.q3, Answers.q4, Answers.q5, Answers.q6]
    all_info['q_mean'] = [db.session.query(func.avg(q)).one()[0] for q in qs]
    print(qs)
    return render_template('results.html', all_info=all_info)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=5000, debug=True)