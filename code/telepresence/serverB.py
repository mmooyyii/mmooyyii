from flask import Flask

app = Flask(__name__)


@app.route('/<a>/<b>')
def add_one(a, b):
    return str(int(a) + int(b))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=28888)
