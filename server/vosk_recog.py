#

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


