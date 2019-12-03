import re

from flask import Flask, render_template, request
app = Flask(__name__, template_folder='templates/')
app.config['student_id'] = 0

RE_INT = re.compile(r'^[-+]?[0-9]+$')
RE_FLOAT = re.compile(r'\d+\.\d+|(?<=angle\s)\d+')

students = []


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
    return {
        'students': students,
    }


@app.route('/api/addStudent', methods=['POST'])
def add_student():
    data = request.json

    name = data.get('name')
    city = data.get('city')
    birthday = data.get('birthday')

    app.config['student_id'] += 1

    students.append({
        'id': app.config['student_id'],
        'name': name,
        'city': city,
        'birthday': birthday,
    })

    return {
        'id': app.config['student_id']
    }


@app.route('/api/updateStudent', methods=['POST'])
def update_student():
    data = request.json

    id_ = int(data.get('id'))
    name = data.get('name')
    city = data.get('city')
    birthday = data.get('birthday')

    for i in range(len(students)):
        if students[i]['id'] == id_:
            students[i]['name'] = name
            students[i]['city'] = city
            students[i]['birthday'] = birthday
    return ''


@app.route('/api/removeStudent', methods=['POST'])
def delete_student():
    data = request.json

    id_ = int(data.get('id'))
    for i in range(len(students)):
        if students[i]['id'] == id_:
            students.remove(students[i])

    return ''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)
