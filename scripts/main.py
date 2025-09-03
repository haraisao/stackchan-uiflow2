import os, sys, io
import M5
from M5 import *
from StackChan import StackChan
from Button import Button
import time


stackchan_0 = None
button_0 = None

wlan = None

def setup():
  global stackchan_0, button_0, wlan

  M5.begin()
  Widgets.setRotation(1)
  Widgets.fillScreen(0x000000)

  stackchan_0 = StackChan()
  wlan = stackchan_0.connect_wlan(10)
  stackchan_0.init_web(80)
  button_0 = Button('Btn1', 0, 220, 100, 20)
  button_0.set_callback('stackchan_0.connect_wlan')


def loop():
  global stackchan_0, button_0, wlan
  M5.update()
  if 0 < (M5.Touch.getCount()):
    button_0.check_tap()
  else:
    button_0.check()
    stackchan_0.update()
    time.sleep_ms(1)


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

