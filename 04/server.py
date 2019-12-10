import os
import re

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab4.db'
db = SQLAlchemy(app)


class StudentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    birthday = db.Column(db.DateTime(timezone=True), nullable=False)

    def jsonify(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'birthday': self.birthday.strftime('%d.%m.%Y'),
        }


db.create_all()
db.session.commit()

RE_INT = re.compile(r'^[-+]?[0-9]+$')
RE_FLOAT = re.compile(r'\d+\.\d+|(?<=angle\s)\d+')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/table', methods=['GET'])
def table():
    return render_template('table.html')


@app.route('/api/distribution', methods=['POST'])
def distribute():
    data = request.json
    text = data.get('text')

    divided = text.split()

    integer_values = list(filter(lambda x: RE_INT.match(x), divided))
    float_values = list(filter(lambda x: RE_FLOAT.match(x), divided))
    another = list(filter(
        lambda x: x not in integer_values + float_values, divided
    ))

    result = (
        f'integers: {integer_values},\tfloat: {float_values},'
        f'\t another{another}'
    )

    return {
        'result': result,
    }


@app.route('/api/getStudents', methods=['GET'])
def get_students():
    students = StudentModel.query.all()
    return {
        'students': [s.jsonify() for s in students],
    }


@app.route('/api/addStudent', methods=['POST'])
def add_student():
    data = request.json

    new_student = StudentModel(
        name=data.get('name'),
        city=data.get('city'),
        birthday=datetime.strptime(data.get('birthday'), '%d.%m.%Y')
    )

    db.session.add(new_student)
    db.session.commit()

    return {
        'id': new_student.id
    }


@app.route('/api/updateStudent', methods=['POST'])
def update_student():
    data = request.json

    student = StudentModel.query.get(int(data.get('id')))

    student.name = data.get('name')
    student.city = data.get('city')
    student.birthday = datetime.strptime(data.get('birthday'), '%d.%m.%Y')

    db.session.commit()

    return ''


@app.route('/api/removeStudent', methods=['POST'])
def delete_student():
    data = request.json

    student = StudentModel.query.get(int(data.get('id')))

    db.session.delete(student)
    db.session.commit()

    return ''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)
