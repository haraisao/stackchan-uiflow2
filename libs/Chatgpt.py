'''
Copyright 2025 Isao Hara, RT Corporation.

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.

'''
import os
from M5 import *
import requests2

import json
import util

#
#
class ChatGPT(object):
  #
  #  Constructor
  #
  def __init__(self):
    self._endpoint = "https://api.openai.com/v1/responses"
    self.api_conf = util.load_conf("/flash/apikey.txt")
    self._apikey = self.api_conf.get('OPENAI_KEY')

    #self._endpoint = "http://localhost:1234/v1/responses"
    #self._apikey = 'lm-studio'

    self.model = 'gpt-5.4-mini'
    self.prompt = ""
    self.prompt = ""

    self.conf = util.load_conf("/chatgpt.txt")
    if "ResponseID" in self.conf:
      self.response_id = self.conf["ResponseID"]
    else:
      self.response_id = ""
  #
  #
  def reset_chat(self):
    self.response_id = ""
  #
  #
  def set_prompt(self, prompt):
    self.prompt=prompt

  #
  #
  def request_openai(self, text):
    url = self._endpoint
    headers = {
        'Authorization': f'Bearer {self._apikey}',
        'Content-Type' : 'application/json; charset=utf-8' }

    data = {
      'model': self.model,
      'input': text,
      'store': True,
      #'tools': [{"type": "mcp", "server_label": "web-search" }]
      #'tools': [{"type": "web_search_preview"}],
      'tools': [{"type": "web_search"}],
    }

    if self.prompt:
      data["instructions"]=self.prompt
      
    if self.response_id:
      data["previous_response_id"] = self.response_id

    try:
      result = requests2.post(url, data=json.dumps(data).encode('utf-8'), headers=headers)
      response = result.json()
      if 'id' in response:
        self.response_id = response['id']
        self.conf["ResponseID"] = response['id']
        util.save_conf("/chatgpt.txt", self.conf)
      return response
    except:
      print ('Error', data, json.dumps(data).encode())
      return ""
    
  def getMessage(self, out):
    res = ""
    for v in out:
      if v["type"] == "output_text":
        res += v["text"]
    return res
  
  def parseResponse(self, response):
    txt=""
    if "output" in response:
      for out_ in response["output"]:
        if out_["type"] == "message":
          txt += self.getMessage(out_["content"])
    return response["id"], txt    
  #
  #
  def talk(self, data):
    response=self.request_openai(data)
    if response:
      res_id, msg = self.parseResponse(response)
      return msg
    return None
  #
  #
  def request(self, txt):
    result = self.talk(txt)
    return result

def main():
  con = ChatGPT()
  con.request("明日の東京では、傘は必要ですか？")

if __name__ == '__main__':
  main()