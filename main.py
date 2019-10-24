from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Hello World =)</h1>\n<h3>init taphee project</h3>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
