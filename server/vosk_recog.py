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
import vosk
import binascii
import json


class VoskRecognizer:
  def __init__(self, model_path="vosk-model-ja-0.22", sample_rate=16000):
    self.model=vosk.Model(model_path)
    self.sample_rate=sample_rate
    self.recognizer=vosk.KaldiRecognizer(self.model, sample_rate)

  def execute(self, data):
    res=self.recognizer.AcceptWaveform(data)
    return self.recognizer.Result()
    #if res:
    #  return self.recognizer.Result()
    #else:
    #  return self.recognizer.PartialResult()

  def request(self, data):
    try:
      bdata = binascii.a2b_base64(data)
      res=self.execute(bdata)
      response=json.loads(res)
      recog_txt=response['text'].replace(' ', '')
      return recog_txt
    except:
      import traceback
      traceback.print_exc()
      return False


