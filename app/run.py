from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests,time
from models.studysets import StudySets

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.context_processor
def inject_pagelinks():
  return dict(user="Wuzzaface",websitename="BootNinja",bloglink="/blog",studylink="/study",homelink="/")

@app.route('/')
def index():
  return render_template('index.html')	

@app.route('/study')
def sets():
  setsrequest = requests.get('https://api.quizlet.com/2.0/users/wuzza_face/sets/?client_id=pyjFb2bnBN')
  setsrequestjson = setsrequest.json()
  currentsets = StudySets(setsrequestjson)
  todaysets = currentsets.getcurrentsets()
  return render_template('study.html',details=todaysets)

@app.route('/blog')
def blog():
  return render_template('blog.html')

if __name__ == '__main__':
    app.run(debug=True)
