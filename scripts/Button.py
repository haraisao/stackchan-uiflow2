import M5

class Button:
  def __init__(self, name, x, y, w, h):
    self.name = name
    self.rect=[x, y, w, h]
    self.tapped=False
    self.callback=self.print_name

  def is_tapped(self, x, y):
    w=self.rect[2]
    h=self.rect[3]
    #print(x, y)
    return (self.rect[0] < x and self.rect[0]+w > x and self.rect[1] < y and self.rect[1]+h > y)

  def check(self):
    if self.callback:
        if self.is_tapped(M5.Touch.getX(), M5.Touch.getY()):
            if self.tapped:
              try:
                self.callback()
              except:
                print("Fail to execute callback")

    else:
        print("Callback not fount")
    self.tapped = False
    return
  
  def check_tap(self):
    if self.is_tapped(M5.Touch.getX(), M5.Touch.getY()):
       self.tapped=True
    return

  def print_name(self, val=None):
    print(self.name)

  def set_callback(self, obj):
    if isinstance(obj, str):
      #print(obj, eval(obj))
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

