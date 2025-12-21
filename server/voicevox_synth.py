#
import os
import sys
import time
from pydub import AudioSegment
#from pydub.playback import play
import pyaudio
from pydub.utils import make_chunks

from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

import soundfile as sf
import resampy
import json
import base64

VOICEVOX_CORE=os.path.join(os.path.dirname(__file__), "voicevox_core")
#
#   
def setup_voicevox(core_dir=VOICEVOX_CORE, model="0.vvm"):
    voicevox_onnxruntime_path = os.path.join(core_dir,
				 "onnxruntime/lib/",
				 Onnxruntime.LIB_VERSIONED_FILENAME)
    open_jtalk_dict_dir = os.path.join(core_dir,
				"dict/open_jtalk_dic_utf_8-1.11")
    synthesizer = Synthesizer(Onnxruntime.load_once(
	 	  filename=voicevox_onnxruntime_path),
		  OpenJtalk(open_jtalk_dict_dir))

    model_ = os.path.join(core_dir, "models/vvms", model)
    with VoiceModelFile.open(model_) as model:
        synthesizer.load_voice_model(model)
    return synthesizer

def save_audio(fname, data):
    with open(fname, "wb") as file:
        file.write(data)
    return 

def load_audio(fname):
    with open(fname, "rb") as file:
        data = file.read()
    return data
#
#
def get_tts_sentence(txt):
    res=[]
    prev=0
    for i in range(len(txt)):
        if txt[i] in ["。", "?", "!", "？", "！"]:
            res.append(txt[prev:(i+1)].strip())
            prev=i+1
    if txt[prev:].strip():
        res.append(txt[prev:].strip())
    return res


#
#
class Voicevox:
    def __init__(self, name="voicevox"):
        #
        # Parameters
        self.core_dir = VOICEVOX_CORE
        
        self.model_file = "0.vvm"
        self.synthesizer = setup_voicevox(self.core_dir, self.model_file)

        self.style_id = 2

    
    def synthesize(self, txt):
        try:
            wav = self.synthesizer.tts(txt, self.style_id)
            fname='synth.wav'
            save_audio(fname, wav)
            x, fs = sf.read(fname)
            y = resampy.resample(x, sr_orig=fs, sr_new=8000)
            sf.write(fname, data=y, samplerate=8000)
            wav2 = load_audio(fname)
            res={'audio': base64.b64encode(wav2).decode()}
            return res
        except:
            import traceback
            traceback.print_exc()
            pass
        return

    def request(self, data):
        print("request:", data)
        param=json.loads(data)
        result=self.synthesize(param['data'])
        return result

def main():
    import comm
    voice_v = Voicevox()
    vosk = VoskRecognizer()
    
    web = comm.create_httpd(8000, "html")
    web.reader.registerCommand('/tts', lambda data: voice_v.request(data))
    web.reader.registerCommand('/vosk', lambda data: vosk.request(data))
    
    web.mainloop=True
    web.run()

if __name__=='__main__':
    main()
