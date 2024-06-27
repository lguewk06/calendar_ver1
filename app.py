# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date

# DB 기본 코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


class calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_day = db.Column(db.String(100), primary_key=False)
    work = db.Column(db.String(100), primary_key=False)
    image_url = db.Column(db.String(100), primary_key=False)

    def __repr__(self):
        return f'{self.work_day} {self.work}'

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day
    first_day = date(2024, 6, 1)
    day_name = first_day.weekday()

    work_list = calendar.query.all()

    date_info = {
        "year": year,
        "month": month,
        "day": day,
        "weekday": day_name
    }

    return render_template('index.html', data=date_info, work=work_list)


@app.route("/work/create/")
def work_create():
    # form에서 보낸 데이터 받아오기
    work_day_receive = request.args.get("date")
    work_receive = request.args.get("event")
    image_receive = request.args.get("image_url")

    # 데이터를 DB에 저장하기
    work = calendar(work_day=work_day_receive, work=work_receive, image_url=image_receive)
    db.session.add(work)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)