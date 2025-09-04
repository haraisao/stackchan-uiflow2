import M5

class Button:
  def __init__(self, name, x, y, w, h):
    self.name = name
    self.rect=[x, y, w, h]
    self.tapped=False
    self.callback=self.print_name
    self.tap_x = -1
    self.tap_y = -1

  def is_tapped(self, x, y):
    w=self.rect[2]
    h=self.rect[3]
    
    return (self.rect[0] < x and self.rect[0]+w > x and self.rect[1] < y and self.rect[1]+h > y)

  def check(self):
    if self.callback:
        if self.is_tapped(self.tap_x, self.tap_y):
            if self.tapped:
              try:
                self.callback()
              except:
                print("Fail to execute callback")
              self.tap_x = -1
              self.tap_y = -1
    else:
        print("Callback not fount")
    self.tapped = False
    return
  
  def check_tap(self):
    self.tap_x = M5.Touch.getX()
    self.tap_y = M5.Touch.getY()
    if self.is_tapped(self.tap_x, self.tap_y):
       self.tapped=True
    return

  def print_name(self, val=None):
    print(self.name)

  def set_callback(self, obj):
    if isinstance(obj, str):
      self.callback = eval(obj)
    else:
      try:
        self.callback = obj.callback
      except:
        self.callback = None
    return

  def update(self):
    M5.update()
    self.check()

