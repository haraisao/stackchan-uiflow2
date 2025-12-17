#
#
import os
import json
import requests2
import binascii
import time

API_KEY = ''
BASE_URL="https://api.dify.ai/v1/chat-messages"

JSON_START='```json\n{'
JSON_END = '}\n```\n'

#
#
class DifyResponse:
  def __init__(self):
    self.message = ''
    self.cmd = ''
    self.request_name = ''
    self.user_name = ''
    self.conversation_id = ''
    self.data = ''
    self.answer=''

  def parse(self, response):
    self.response_ = response
    info = response.info()
    data = response.data.decode('utf-8')
    if info['Content-Type'] == 'application/json':
      self.data = json.loads(data)
      try:
        self.conversation_id = self.data['conversation_id']
      except:
        print("ERROR", self.data)
    else:
      self.data = data
    return
  
  def parse_json(self, answer):
    st_pos=answer.find(JSON_START)
    en_pos=answer.find(JSON_END)
    if st_pos < 0 or en_pos < 0:
      try:
        return json.loads(answer), ""
      except:
        print("___ Fail to pase JSON____")
        return None, answer
    msg=answer[:st_pos]
    res = json.loads("{" + answer[st_pos+len(JSON_START):en_pos] +"}")
    return res, msg

#
#
#
class Dify(object):
  #
  #  Constructor
  #
  def __init__(self, name='robot'):
    self._endpoint = BASE_URL
    self._apikey = API_KEY
    self.conversation_id=""
    self.prompt = ""
    self.upload_file_id=""
    self.name = name

  #
  #
  def reset_chat(self):
    self.conversation_id=""
    self.name_card_inputs = {}
    return

  #
  #
  def request_dify(self, query, user, inputs={}, endpoint="/chat-messages"):    
    url = self._endpoint+endpoint

    headers = {
          'Authorization': f'Bearer {self._apikey}',
          'Content-Type': 'application/json'
        }
    data = {
        "inputs": inputs,
        "query": query,
        "response_mode": "blocking",
        "user": user,
        "conversation_id": self.conversation_id,
    }

    try:
      st=time.time()
      response = requests2.post(url, json=data, headers=headers)
      return self.gen_response(response)
    except:
      print ('Error')
      return ""

  #
  #
  def request(self, msg, endpoint="/chat-messages"):
    response=self.request_dify(msg, self.name, endpoint=endpoint)
    #
    # extract message
    self.conversation_id = response.conversation_id
    return response

  def gen_response(self, response):
    res=DifyResponse()
    res.parse(response)
    return res
