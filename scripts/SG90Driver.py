#
#
from M5 import *
import machine
import time
import math

def sign(x):
    return (x > 0) - (x < 0)

class SG90Driver:
  def __init__(self, offset=56):
    self.min = 500 * 65535 // 20000
    self.max = 2500 * 65535 // 20000
    self.zero = (1500+offset) * 65535 // 20000
    self.ddeg = (self.max -self.min) / 180.0
    self.delay=0.02
    self.motor(True)

  def create_pwm(self, pin):
    return machine.PWM(pin, freq=50, duty_u16=self.zero)

  def move_direct(self, h_deg, v_deg):
    self.h_motor.duty_u16(self.zero + int(self.ddeg * h_deg))
    self.v_motor.duty_u16(self.zero + int(self.ddeg * v_deg))
    self.current_pos=[h_deg, v_deg]
    return

  def move(self, h_deg, v_deg, tm=0.5):
    h_deg = max(min(h_deg, 90), -90)
    v_deg = max(min(v_deg, 5), -30)

    n = int(tm / self.delay)
    h_dg = (h_deg - self.current_pos[0]) / n
    v_dg = (v_deg - self.current_pos[1]) / n

    for x in range(0, n):
      h_target_ = self.current_pos[0] + h_dg
      v_target_ = self.current_pos[1] + v_dg
      self.h_motor.duty_u16(self.zero + int(self.ddeg * h_target_))
      self.v_motor.duty_u16(self.zero + int(self.ddeg * v_target_))
      time.sleep(self.delay)
      self.current_pos = [h_target_, v_target_]
    return

  def motor(self, flag=True):
    if flag:
        self.h_motor=self.create_pwm(2) # PortA-> 2, PortC -> 17
        self.v_motor=self.create_pwm(9)  # PortB -> 9
        self.current_pos=[0,0]
    else:
        self.h_motor.deinit()
        self.v_motor.deinit()
    return
