import os, sys, io
import M5
from M5 import *
from Button import Button
from StackChan import StackChan


label0 = None
stackchan_0 = None
button_0 = None


def setup():
  global label0, stackchan_0, button_0

  M5.begin()
  Widgets.setRotation(1)
  Widgets.fillScreen(0x222222)
  label0 = Widgets.Label("label0", 228, 9, 1.0, 0xffffff, 0x222222, Widgets.FONTS.EFontJA24)

  Widgets.setRotation(1)
  stackchan_0 = StackChan()
  stackchan_0.connect_wlan('RT4F')
  stackchan_0.init_web(80)
  button_0 = Button('Btn1', 0, 220, 100, 20)
  button_0.set_callback('stackchan_0.connect_wlan')


def loop():
  global label0, stackchan_0, button_0
  M5.update()
  if 0 < (M5.Touch.getCount()):
    button_0.check_tap()
  else:
    button_0.check()
    stackchan_0.update()


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
