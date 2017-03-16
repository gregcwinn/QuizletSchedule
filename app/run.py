from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests,time

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	user = 'wuzzaface'
	return render_template('index.html',title='Home',user=user)	

@app.route('/sets')
def sets():
	setsrequest = requests.get('https://api.quizlet.com/2.0/users/wuzza_face/sets/?client_id=pyjFb2bnBN')
	setsrequestjson = setsrequest.json()
	titledateurl=([(item["title"],time.strftime('%m-%d-%Y', time.localtime(item["created_date"])),item["url"]) for item in setsrequestjson])
	return render_template('bootsets.html',details=titledateurl)

if __name__ == '__main__':
    app.run(debug=True)
