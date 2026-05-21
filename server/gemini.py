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
import requests

import json

def load_contents(fname):
  try:
    with open(fname, "r") as file:
      data = file.read()
    return data
  except:
    return ""

def save_contents(fname, contents):
  try:
    with open(fname, "w") as file:
      file.write(contents)
    return
  except:
    print("Fail to write contents:", fname)
    return
class Gemini(object):
  #
  #  Constructor
  #
  def __init__(self, apikey):
    self._endpoint = "https://generativelanguage.googleapis.com/v1beta/interactions"
    self._apikey = apikey

    self.model = "/gemini-3.5-flash"
    self._lang = 'ja-JP'
    self.prompt = ""
    self.load_interacation_id()
    self.generation_config= {"thinking_level": "low"}
    self.functions = []
  #
  #
  def reset_chat(self):
    self.previous_interaction=""
    return

  def set_interaction_id(self, txt=""):
    self.previous_interaction=txt

  def set_prompt(self, prompt):
    self.prompt=prompt
    return

  def get_response_text(self, result):
    for res in result["steps"]:
      if res["type"] == "model_output":
        txt = ""
        for x in res["content"]:
          if x["type"] == "text":
            txt += x["text"]
        return result["id"], txt
    return None

  def get_response_func(self, result):
    try:
      for res in result["steps"]:
        if res["type"] == "function_call":
          return result["id"],res
      return None
    except:
      print(result)
  #
  #
  def load_mcp_func(self, fname):
    func=load_contents(fname)
    if func:
      self.functions.append(func)

  def save_interacation_id(self, fname="gemini.txt"):
    save_contents(fname, self.previous_interaction)

  def load_interacation_id(self, fname="gemini.txt"):
    self.previous_interaction = load_contents(fname)

  #
  #
  def request_gemini(self, text, save_id=True):
    url = self._endpoint + "?key=" + self._apikey
    headers = { 'Api-Revision': '2026-05-20',
                'Content-Type' : 'application/json' }
    data = {
      "model": self.model,
      "input": text,
    }

    if self.generation_config:
      data["generation_config"] = self.generation_config

    if self.previous_interaction:
      data["previous_interaction_id"] = self.previous_interaction
      
    if self.prompt:
      data["system_instruction"] =  self.prompt
    #
    #
    data["tools"] = [
            {"type": "google_search" }
            ]
    for fn in self.functions:
      data["tools"].append(fn)
    #
    #
    try:
      result = requests.post(url, data=json.dumps(data).encode('utf-8'), headers=headers)
      response = result.json()
      if 'id' in response:
        self.previous_interaction = response['id']
        if save_id:
          self.save_interacation_id()
      return response
    except:
      print ('Error', data)
      print ('Error', json.dumps(data).encode())
      return ""
    
  #
  def response_mcp(self, interaction, funcall, result, save_id=True):
    url = self._endpoint + "?key=" + self._apikey
    headers = { 'Api-Revision': '2026-05-20',
                'Content-Type' : 'application/json' }

    data = {
      "model": self.model,
      "input": [{
          "type": "function_result",
          "name": funcall["name"],
          "call_id": funcall["id"],
          "result": [ {"type": "text", "text": json.dumps(result)}]
        },
      ],
      "previous_interaction_id": interaction
    }

    try:
      result = requests.post(url, data=json.dumps(data).encode('utf-8'), headers=headers)
      response = result.json()
      if 'id' in response:
        self.previous_interaction = response['id']
        if save_id:
          self.save_interacation_id()
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

  def mcp_response(self, result):
    if self.mcp_funcall:
      interaction = self.mcp_funcall[0]
      funcall = self.mcp_funcall[1]
      res=self.response_mcp(interaction, funcall, result)
      response_text = self.get_response_text(res)
      
      print(response_text)
      self.mcp_funcall = None
  #
  #
  def request(self, txt):
    result = self.request_gemini(txt)
    mcp_funcall = self.get_response_func(result)
    if mcp_funcall:
      self.mcp_funcall = mcp_funcall
      print(mcp_funcall)
      self.mcp_response({"result": "Finished"})
      return
    response_text = self.get_response_text(result)
    print(response_text[1])
  