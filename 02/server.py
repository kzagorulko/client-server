import re

from flask import Flask, render_template
app = Flask(__name__, template_folder='.')

RE_INT = re.compile(r'^[-+]?[0-9]+$')
RE_FLOAT = re.compile(r'\d+\.\d+|(?<=angle\s)\d+')


@app.route('/', methods=['GET'])
def index():
    return render_template(
            'index.html', int_answer='', float_answer='',
            str_answer=''
        )


@app.route('/<text>', methods=['GET'])
def distribute(text):
    divided = text.split()

    integer_values = list(filter(lambda x: RE_INT.match(x), divided))
    float_values = list(filter(lambda x: RE_FLOAT.match(x), divided))
    another = list(filter(
        lambda x: x not in integer_values + float_values, divided
    ))

    return render_template(
        'index.html', int_answer=integer_values, float_answer=float_values,
        str_answer=another
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
