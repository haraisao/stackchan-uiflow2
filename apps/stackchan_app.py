import os, sys, io
import time
import M5
from M5 import *
from hardware import sdcard

if not "sd" in os.listdir("/"):
  sdcard.SDCard(slot=3, width=1, miso=35, mosi=37, sck=36, cs=4)

sys.path.append('/sd/scripts')

from StackChan import StackChan
from Button import Button

stackchan_0 = None
button_0 = None
button_1 = None
button_2 = None
button_3 = None

def setup():
  global stackchan_0, button_0, button_1, button_2, button_3
  M5.begin()
  Widgets.setRotation(3)
  Widgets.fillScreen(0x000000)
  stackchan_0 = StackChan()
  stackchan_0.init_web(80)
  button_0 = Button('Btn1', 0, 220, 100, 20)
  button_0.set_callback('stackchan_0.start_web_server')
  button_1 = Button('Btn2', 220, 220, 100, 20)
  button_1.set_callback('stackchan_0.show_battery_level')
  button_2 = Button('Btn3', 130, 60, 60, 60)
  button_2.set_callback('stackchan_0.start_dialog')
  button_3 = Button('Btn4', 0, 0, 60, 60)
  button_3.set_callback('stackchan_0.toggle_rand_motion')

def loop():
  global stackchan_0, button_0, button_1, button_2, button_3
  M5.update()
  if 0 < (M5.Touch.getCount()):
    if button_0.check_tap():
      button_0.check()
    elif button_1.check_tap():
      button_1.check()
    elif button_2.check_tap():
      button_2.check()
    elif button_3.check_tap():
      button_3.check()
    else:
      stackchan_0.clear_msg()
  else:
    stackchan_0.update()
    time.sleep_ms(100)

if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
