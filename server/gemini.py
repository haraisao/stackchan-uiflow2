#
#
import os
import requests

import json

class Gemini(object):
  #
  #  Constructor
  #
  def __init__(self, apikey):
    self._endpoint = "https://generativelanguage.googleapis.com/v1beta/models"
    self._apikey = apikey

    self.model = "/gemini-2.5-flash:generateContent"
    self._lang = 'ja-JP'
    self.chat_history=[]
    self.prompt = ""
  #
  #
  def reset_chat(self):
    self.chat_history=[]
    return
  
  def set_prompt(self, prompt):
    self.prompt=prompt
    return
  #
  #
  def gen_chat_content(self, txt, role="user"):
    res={
          "parts" : [{ "text": txt }],
          "role": role
        }
    self.chat_history.append(res)
    return res

  #
  #
  def get_system_chat_content(self, result):
    try:
      res=result['candidates'][0]['content']['parts'][0]['text']
      self.gen_chat_content(res, 'model')
      return res
    except:
      print(result)
      return "失敗しました"
  #
  #
  def request_gemini(self, text):
    url = self._endpoint+self.model
    headers = { 'x-goog-api-key': self._apikey,
                'Content-Type' : 'application/json; charset=utf-8' }

    self.gen_chat_content(text)

    data = {
      "contents": self.chat_history,
    }
    if self.prompt:
      data["system_instruction"] = {
          "parts" : [{
           "text": self.prompt
         }],
         "role" : "model"
      }
    #
    #
    data["tools"] = [
            { "url_context": {} },
            { "google_search": {} }
            ]
    try:
      result = requests.post(url, data=json.dumps(data).encode('utf-8'), headers=headers)
      response = result.json()
      return response
    except:
      print(result.json())
      print ('Error', data, json.dumps(data).encode())
      return ""
  #
  #
  def talk(self, data):
    response=self.request_gemini(data)
    if response:
      return response
    return None
  #
  #
  def request(self, txt):
    result = self.talk(txt)
    if result:
      return self.get_system_chat_content(result)
    return ""

#
#
if __name__ == '__main__':
  key=''
  gemini=Gemini(key)
  gemini.set_prompt("あたなは、小さなスーパーロボット「スタックチャン」です。現在、東京にいます。対話の応答は、東京にいることを前提に、２０字以内で答えてください。")
  res=gemini.request("こんにちは")
  #res_str=gemini.get_system_chat_content(res)
  print(res)