from flask import Flask,request, session, g, redirect, url_for, abort, render_template, flash
from flask import jsonify
import json
from config.config_local import *

import apiai

app = Flask(__name__)


app.config.from_object('config.config_local.DevelopmentConfig')
app.config.from_object(__name__)
app.config.from_envvar('FORTYTWO_SETTINGS', silent=True)

@app.route('/')
def index():
    last_questions=1
    return render_template('index.html',last_questions=last_questions)


@app.route('/send', methods=['POST'])
def send():
    try:

        text =request.form["text"]
        print(text)
        ai = apiai.ApiAI(app.config.get("APIAI_CLIENT_ACCESS_TOKEN"))
        ai_request = ai.text_request()
        ai_request.lang = 'it'  # optional, default value equal 'en'
        ai_request.session_id = app.config.get("APIAI_USER_ACCESS_TOKEN")
        ai_request.query = text
        print("ready...")
        response = ai_request.getresponse()
        print("response")
        print(response)
        print(response.status)
        if (response.status == 200):
            str = response.read().decode("utf8")
            print(str)
            r = json.loads(str)
            print("read")
            print(r)
            return jsonify(answer=r['result']['fulfillment']['speech'], last_questions=None, answer_prob=1.0)
        else:
            return jsonify(answer="I had some problems with my brain", last_questions=None, answer_prob=1.0)
    except:
        raise
        return jsonify(answer="ERROR: I had some problems with my brain", last_questions=None, answer_prob=1.0)



if __name__ == '__main__':
    app.run()