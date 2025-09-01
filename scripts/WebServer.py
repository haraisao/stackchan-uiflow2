#
#
from M5 import *
import machine
import time
import comm


class WebServer:
  def __init__(self, port=80, top="/sd/html"):
    if type(port) == str: port = int(port)
    self.port = port
    self.reader = comm.HttpReader(top)
    self.server=comm.SocketServer(self.reader, "Web", "", port)
  
  def renew(self):
    self.server.stop()
    self.server=comm.SocketServer(self.reader, "Web", "", self.port)
    return
  
  def registerCommand(self, name, func):
    if type(func) is str:
      try:
        func = eval(func)
        print(func)
      except:
        print("ERROR to register:", func)
        return

    self.server.reader.registerCommand(name, func)
    return
  
  def start(self):
    self.server.start()
    return

  def stop(self):
    try:
      self.server.terminate()
    except:
      pass
    return
  

  