#
from flask import Flask, render_template, session, request, redirect
from flask import jsonify, session, make_response
from flask import Blueprint

import requests
from vosk_recog import VoskRecognizer
from voicevox_synth import Voicevox
from gemini import Gemini
import datetime
import os
import yaml


def load_yaml(fname):
    config=None
    try:
        with open(fname, 'r') as yml:
            config=yaml.safe_load(yml)
    except:
        pass
    return config

DOCUMENT_ROOT=os.environ.get('DOCUMENT_ROOT', os.getcwd()+'/html/')

TEMPLATE_ROOT=DOCUMENT_ROOT
print(DOCUMENT_ROOT, TEMPLATE_ROOT)

blueprint_app=Blueprint('html', __name__, static_url_path='', static_folder=DOCUMENT_ROOT)
app=Flask(__name__, template_folder=TEMPLATE_ROOT, static_folder=None)
app.register_blueprint(blueprint_app)
app.config['JSON_AS_ASCII'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.secret_key='AI_Stackchan'
app.permanent_session_lifetime = datetime.timedelta(hours=16)

KEY_FILE=os.environ.get('KEY_FILE', 'conf/application_key.yaml' )
config=load_yaml(KEY_FILE)

voice_v = Voicevox()
vosk = VoskRecognizer()

#key=config['GEMINI']
#gemini=Gemini(key)
#gemini.set_prompt("あたなは、小さなスーパーロボット「スタックチャン」です。現在、東京にいます。対話の応答は、東京にいることを前提に、２０字以内で答えてください。")


#
#
# REST_API
@app.route('/vosk', methods=["POST"])
def rest_vosk():
    response = vosk.request(request.data)
    return jsonify(response)

@app.route('/tts', methods=["POST"])
def rest_tts():
    response = voice_v.request(request.data)
    return jsonify(response)

#@app.route('/talk_str', methods=["POST"])
#def rest_talk_str():
#    txt=request.json['data']
#    result = gemini.request(txt)
#    response={'response': result}
#    return jsonify(response)

if __name__=='__main__':
    server_port = os.environ.get('PORT', '8000')
    app.run(debug=False, port=server_port, host='0.0.0.0')
