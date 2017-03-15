from flask import Flask
from subprocess import call
app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/sets')
def sets():
	results = call(['python','getpublicsets.py'])
	return results

if __name__ == '__main__':
    app.run(debug=True)
