from flask import Flask,request, session, g, redirect, url_for, abort, render_template, flash
from flask import jsonify
import json
from config.config_local import *

import apiai

app = Flask(__name__)


app.config.from_object('config.config_local.DevelopmentConfig')
app.config.from_object(__name__)
app.config.from_envvar('FORTYTWO_SETTINGS', silent=True)


def aianswer(text):
    try:
        ai = apiai.ApiAI(app.config.get("APIAI_CLIENT_ACCESS_TOKEN"))
        ai_request = ai.text_request()
        ai_request.lang = 'it'
        ai_request.session_id = app.config.get("APIAI_USER_ACCESS_TOKEN")
        ai_request.query = text
        response = ai_request.getresponse()
        if (response.status == 200):
            str = response.read().decode("utf8")
            r = json.loads(str)
            return jsonify(answer=r['result']['fulfillment']['speech'], last_questions=None, answer_prob=1.0)
        else:
            return jsonify(answer="I had some problems with my brain", last_questions=None, answer_prob=1.0)
    except:
        return jsonify(answer="ERROR: I had some problems with my brain", last_questions=None, answer_prob=1.0)



@app.route('/')
def index():
    last_questions=1
    return render_template('index.html',last_questions=last_questions)


@app.route('/send', methods=['POST'])
def send():
    text = request.form["text"]
    return aianswer(text)


@app.route('/slack', methods=['POST'])
def inbound():
    retstring =""
    print(request.form.get("channel_name"))
    if request.form.get('token') == app.config.get("SLACK_WEBHOOK_SECRET"):
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        response = aianswer(text)
        str = response.get_data().decode("utf8")
        r = json.loads(str)
        #print(r["answer"])
        retstring = r["answer"]
    else:
        retstring=":-("
    return retstring

if __name__ == '__main__':
    app.run()