
from threading import Thread
import sys
import select

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
      ans = ""
      while self.running:
        r = select.select([sys.stdin], [], [], 0.5)
        if sys.stdin in r[0]:
          w = sys.stdin.read(1)
          ans = (ans + w).strip()
          print "|%s|" % w
          if "\n" in w:
            break
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
