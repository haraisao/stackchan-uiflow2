'''
  Stack-chan Main Class
'''
import M5
import json
import time
import binascii
import camera
import dl
import gc

import Face
import util
import WebServer

#
# Stack-chan Main
class StackChan:
  #
  #
  def __init__(self):
    util.mount_sd()
    gc.enable()
    try:
      self.config=util.load_json("/sd/stackchan.json")
    except:
      self.config={}
    # WLAN
    self.wlan = util.connect_wlan()
    self.camera_setupted = False
    self.tracking_flag = False

    if self.config.get('camera_setup'):
      self.setup_camera()

    #
    # face, motors, TTS client, ASR client
    self.face=Face.Face()
    self.web_server=None
    self.motor=None
    self.set_motor()
    self.tts=None
    self.set_tts()
    self.asr=None
    self.set_asr()
    self.dialog=None
    self.setup_dialog()

    self.event_time=time.time()
    self.debug_time=time.time()
    self.debug = 0
  #
  # Create web server
  def init_web(self, n=80, start=False):
    if self.config.get('web_server'):
      try:
        port = int(self.config['web_server'])
      except:
        port = n
    else:
      port = n
  
    self.web_server=WebServer.WebServer(port)
    #
    # Register REST API
    self.web_server.registerCommand("/move", self.set_goal_position)
    self.web_server.registerCommand("/face", self.face.set_face_id)
    self.web_server.registerCommand("/get_camera_image", self.capture_image)
    self.web_server.registerCommand("/set_message", self.set_message)
    self.web_server.registerCommand("/command", self.request_command)
    if self.tts:
        self.web_server.registerCommand("/tts", self.tts.set_request)
    if self.asr:
        self.web_server.registerCommand("/asr", self.asr.set_request)

    #if start:
    #  self.start_web_server()
    return
  #
  # Start web service thread.
  def start_web_server(self):
    if self.web_server is None:
      self.init_web(start=False)

    state_=self.web_server.toggle_state()
    
    if self.isconnected_wlan():
        self.face.print_info("IP:" + self.wlan.ifconfig()[0]+ ", "+state_)
    else:
      if self.connect_wlan(10):
        self.face.print_info("IP:" + self.wlan.ifconfig()[0] + ", "+state_)
    return
  
  def request_command(self, data):
    param=json.loads(data)
    if param['cmd'] == 'detect_face':
      self.tracking_face()
      return True
    elif param['cmd'] == 'face_tracking':
      self.tracking_flag=param['data']
      return True
    return False
  #
  # camera
  def setup_camera(self):
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)
    if 'vflip' in self.config:
      camera.set_vflip(self.config['vflip'])

    self.face_detector = dl.ObjectDetector(dl.model.HUMAN_FACE_DETECT)
    self.camera_setupted = True 
    return
  #
  #
  def detect_face(self, data=""):
    if not self.camera_setupted : return None 
    img = camera.snapshot()
    detection_result = self.face_detector.infer(img)
    face_pos=[]
    if detection_result:
      for res in detection_result:
        #kp = res.keypoint()
        face_pos.append([res.x(), res.y(), res.w(), res.h()])
    return face_pos
  #
  #
  def tracking_face(self):
    if not self.tracking_flag:
      time.sleep_ms(50)
      return 
    face_pos_ = self.detect_face()
    if face_pos_ :
      pos_ =face_pos_[0]
      center_x = pos_[0]+pos_[2]//2
      center_y = pos_[1]+pos_[3]//2
      print("Face:", center_x, center_y, pos_[2], pos_[3])
      if pos_[3] > 60:
        dx = center_x - 160
        dy = center_y - 120
        cpos = self.motor.current_pos
        if abs(dx) > 10 or  abs(dy) > 10: 
          dx_deg = cpos[0] + dx / 20.0
          dy_deg = cpos[1] + dy / 20.0
          #print(cpos, dx, dy, dx_deg, dy_deg)
          self.motor.motor(True)
          self.motor.move(dx_deg, dy_deg)
      if pos_[3] > 160:
        self.start_dialog()
    return
  #
  #
  def clear_msg(self):
    self.face.print_info()
    self.face.print_message()
    return
  #
  # Setup motor driver
  def set_motor(self):
    try:
      if self.config['motor'] == 'Dynamixel':
        import DynamixelDriver
        self.motor = DynamixelDriver.DynamixelDriver()
      elif self.config['motor'] == 'SG90':
        import SG90Driver
        try:
          self.motor = SG90Driver.SG90Driver(
                          h_port=int(self.config['sg90_pan']),
                          v_port=int(self.config['sg90_tilt']))
        except:
          self.motor = SG90Driver.SG90Driver()
      else:
        self.motor = None
    except:
      self.motor = None
    return
  #
  # Setup Text-to-speach(TTS) client
  def set_tts(self, name='google'):
    tts_name = name
    if self.config.get('tts'):
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
    
    if self.tts:
      self.tts.parent=self
    return
  #
  # Setup Automatic-speech-recognition(ASR) client
  def set_asr(self, name='google'):
    asr_name = name
    if self.config.get('asr'):
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

    if self.asr:
      self.asr.parent = self
    return
  #
  #
  def setup_dialog(self, name='gemini'):
    dialog_name = name
    if self.config.get('dialog'):
      dialog_name = self.config['dialog']
  
    if dialog_name == 'gemini':
      import Gemini
      try:
        self.dialog = Gemini.Gemini()
      except:
        pass
    elif dialog_name == 'openai':
      import Chatgpt
      try:
        self.dialog = Chatgpt.ChatGPT()
      except:
        pass
    elif dialog_name == 'lmstudio':
      import LmStudio
      try:
        self.dialog = LmStudio.LmStudio(self.config['lmstudio_host'])
      except:
        pass
    else:
      print("No such classe", dialog_name)
    if self.dialog and self.config.get('prompt'):
      self.dialog.set_prompt(self.config['prompt'])
    return
  #
  # Connect Wireless LAN
  def connect_wlan(self, trial=10):
    for _ in range(trial):
      if self.wlan and self.wlan.isconnected():
        self.face.print_info("IP:" + self.wlan.ifconfig()[0])
        return True
      else:
        self.face.print_info("Connecting...")
        self.wlan = util.connect_wlan(self.wlan)
        time.sleep(1)
    self.face.print_info("WLAN not connected")
    return False
  #
  # Check connection of wireless LAN
  def isconnected_wlan(self):
    if self.wlan:
      return self.wlan.isconnected()
    return False
  #
  # Servo on/off (for Dynamixel motor)
  def set_torque(self, val):
    try:
      if isinstance(val, str): val = eval(val)
      self.motor.setTorque(val)
    except:
      pass
    return True
  #
  # Teminate web service
  def stop_web(self):
    self.web_server.stop()
    return
  #
  # Tarminate web service and motor control
  def stop(self):
    self.web_server.stop()
    self.set_torque(False)
    return
  #
  # Set goal position: pose=[Pan(degree), Tilt(degree)]
  def set_goal_position(self, pose):
    if self.motor:
      if isinstance(pose, str):
        pose = eval(pose)
      self.motor.move(pose[0], pose[1])
      return True
    return False
  #
  # Set goal posirion
  def move(self, p_deg, t_deg):
    self.motor.move(p_deg, t_deg, force=True)
    return
  #
  # Show ASR result
  def show_asr_result(self, result):
    if result and result.get('error') == '':
      self.print_info(result.get('result'))
    return True
  #
  #
  def print_info(self,msg='',color=0xffff00):
    self.face.print_info(msg,color)

  def print_message(self,msg='',color=0xffffff):
    self.face.print_message(msg,color)
  #
  # Capture an image
  def capture_image(self, arg):
    try:
      frame = camera.snapshot()
      print("capture image")
      raw_bytes = frame.bytearray()
      encoded = binascii.b2a_base64(raw_bytes, newline=False).decode()
      response = {
          'width': frame.width(),
          'height': frame.height(),
          'data': encoded
      }
    except:
      print("Error: Camera")
      response = {
          'width': 0,
          'height': 0,
          'data': ''
      }
    gc.collect()
    gc.mem_free()
    return response
  #
  # Set message
  def set_message(self, data):
    try:
      msg = json.loads(data)
      if msg['type'] == 'info':
        self.face.info = msg['message']
      elif msg['type'] == 'message':
        self.face.message = msg['message']
      else:
        self.face.message=''
        self.face.info=''
    except:
      pass
    return True
  #
  #
  def show_battery_level(self):
    self.face.print_message('Battery: %d %%' % M5.Power.getBatteryLevel())
    self.face.random_face()
    return
  #
  #
  def start_dialog(self):
    data = '{"max_seconds": 6, "threshold": 41, "max_count": 1}'
    self.asr.set_request(data)
    return
  #
  #
  def toggle_rand_motion(self):
    if self.motor:
      self.motor.toggle_rand_motion()
      if self.motor.rand_motion:
        self.face.print_message("Motion On")
      else:
        self.face.print_message("Motion Off",0xff8888)
  #
  #
  def toggle_tracking(self):
    if self.motor:
      if self.tracking_flag:
        self.face.print_message("Tracking Off", 0xff8888)
        self.tracking_flag=False
      else:
        self.tracking_flag=True
        self.face.print_message("Tracking On",0x88ff88)
  #
  #
  def set_face_id(self, id):
    self.face.set_face_id(id)
    return
  #
  # Spin once
  def update(self):
    debug = time.time() - self.debug_time
    if self.debug != debug:
      #print(debug)
      self.debug = debug
    if self.web_server:
      self.web_server.update()
    self.face.update()
    if self.camera_setupted:
      self.tracking_face()
    #return
    #
    if self.motor:
      if self.motor.update():
        #print("Debug", debug)
        return
    #
    if self.asr:
      res=self.asr.check_request()
      if res and self.dialog and res['result'] != '':
          self.face.print_info("考え中…")
          result=self.dialog.request(res['result'])
          try:
            print(result)
            if result == "ありがとう":
              self.dialog.reset_chat()
            self.tts.set_request(result.replace('*', ''))
          except:
            print(result)
      else:
        if res is None:
          pass
          #self.tts.set_request("対話終了")
        elif res and res['result'] == '':
          self.tts.set_request("何？")
        self.show_asr_result(res)
    if self.tts:
      self.tts.check_request()
    return
