#import M5
import Face
import util
import json

#import Voicevox
#import VoskAsr

#import MeloTts
#import Gasr
import Gtts

import WebServer



class StackChan:
  def __init__(self):
    util.mount_sd()
    try:
      self.config=json.loads(util.get_file_contents("/sd/stackchan.json"))
    except:
      self.config={}
    # WLAN
    self.wlan_config = util.get_wlan_conf()
    if 'ap_name' in self.config:
      self.ap_name = self.config['ap_name']
    else:
      self.ap_name = list(self.wlan_config.keys())[0]
    self.wlan = None
    #
    # 
    self.face=Face.Face()
    self.set_motor()
    self.set_tts()
    self.set_asr()

  def init_web(self, n=80):
    if  'web_server' in self.config:
      try:
        port = int(self.config['web_server'])
      except:
        port = n
    else:
      port = n

    self.web_server=WebServer.WebServer(port)
    self.web_server.registerCommand("/move", self.set_goal_position)
    self.web_server.registerCommand("/face", self.face.set_face_id)
    if self.tts:
        self.web_server.registerCommand("/tts", self.tts.set_request)

    if self.asr:
        self.web_server.registerCommand("/asr_local", self.do_asr_process)
        self.web_server.registerCommand("/asr", self.asr)

    self.start_web_server()
    return
  
  def start_web_server(self):
    if self.isconnected_wlan():
        self.web_server.start()
    return

  def set_motor(self):
    try:
      if self.config['motor'] == 'Dynamixel':
        import DynamixelDriver
        self.motor = DynamixelDriver.DynamixelDriver()
      elif self.config['motor'] == 'SG90':
        import SG90Driver
        self.motor = SG90Driver.SG90Driver()
      else:
        self.motor = None
    except:
      self.motor = None
    return
  
  def set_tts(self):
    tts_name = 'google'
    if 'tts' in self.config:
      tts_name = self.config['tts']

    if tts_name == 'voicevox':
      import Voicevox
      self.tts = Voicevox.Voicevox(self.config['tts_ip'])
    elif tts_name == 'melo_tts':
      import MeloTts
      self.tts = MeloTts.MeloTts()
    else:
      import Gtts
      self.tts = Gtts.Gtts()

  def set_asr(self):
    asr_name = 'google'
    if 'asr' in self.config:
      asr_name = self.config['asr']

    if asr_name == 'vosk':
      import VoskAsr
      self.asr = VoskAsr.VoskAsr(self.config['asr_ip'])
    elif asr_name == 'llm_asr':
      print("LLM-ASR not supported")
      self.asr = None
    elif asr_name == 'llm_whisper':
      print("LLM-Wisper not supported")
      self.asr = None
    else:
      import Gasr
      self.asr = Gasr.Gasr()    
  
  def connect_wlan(self, name=None, tryal=10):
    if name is None:
      name=self.ap_name
    if self.wlan is None:
      self.wlan=util.setup_wlan(name,n=5)
    else:
      util.connect_wlan(self.wlan, name, 5)

    if not self.isconnected_wlan():
      for _ in range(tryal):
        util.connect_wlan(self.wlan, name, 5)
        if self.isconnected_wlan(): break

    if self.wlan.isconnected():
      self.face.print_info("IP:" + self.wlan.ifconfig()[0])
    else:
      self.face.print_info("WLAN not connected")

  def isconnected_wlan(self):
    if self.wlan:
      return self.wlan.isconnected()
    return False

  def set_torque(self, val):
    try:
      if isinstance(val, str): val = eval(val)
      self.motor.setTorque(val)
    except:
      pass
    return True

  def stop_web(self):
    self.web_server.stop()
    return

  def stop(self):
    self.web_server.stop()
    self.set_torque(False)
    return

  def set_goal_position(self, pose):
    if self.motor:
      if isinstance(pose, str):
        pose = eval(pose)
      self.motor.move(pose[0], pose[1])
      return True
    return False

  def do_asr_process(self):
    if self.asr:
      result = self.asr.do_process()
      if result and result['error'] == '':
        self.face.print_info(result['result'])

  def move(self, p_deg, t_deg):
    self.motor.move(p_deg, t_deg, True)
    return
  
  def update(self):
    #if self.web_server:
    #  self.web_server.server.spin_once(0.3)
    self.face.update()
    if self.motor:
      self.motor.update()
    if self.tts:
      self.tts.check_request()


