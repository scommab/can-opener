
from threading import Thread

class Can(Thread):
  def __init__(self, id, opener, key):
    Thread.__init__(self)
    self.key = key
    self.id = id
    self.opener = opener
    self.running = True
    pass

  def run(self):
    while self.running:
      print "Enter Msg"
      ans = raw_input().strip()
      self.opener(self.id, ans)

  def stop(self):
    self.running = False

  def setKey(self, key):
    self.key = key


if __name__ == "__main__":
  cans = {}
  def opener(id, ans):
    if id not in cans:
      return
    if ans == "q":
      cans[id].stop()  
  c = Can(1, opener, "non-real")
  cans[c.id] = c
  c.start()
