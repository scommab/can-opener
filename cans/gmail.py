
from threading import Thread
import sys
import imaplib
import time

class Can(Thread):
  def __init__(self, id, config, opener, key):
    Thread.__init__(self)
    self.key = key
    self.config = config
    self.id = id
    self.opener = opener
    self.running = True
    pass

  def run(self):
    try:
      user = self.config.get('email', 'username')
      passwd = self.config.get('email', 'password')
    except:
      # failed look up: abore running
      return

    while self.running:
      m = imaplib.IMAP4_SSL('imap.gmail.com')
      m.login(user, passwd)
      count = m.select('Inbox')[1][0]
      r, messages = m.search(None, '(UNSEEN)')
      #print messages
      for uid in messages[0].split(" "):
        r, data = m.fetch(uid, '(ENVELOPE)')
        data = data[0]
        subject = data.split('"')[3]
        if str(self.key) in subject:
          r, body = m.fetch(uid, '(BODY[TEXT])')
          body = body[0][1].strip()
          #print subject
          #print body
          self.opener(self.id, body)
      m.logout()
      time.sleep(15)

  def stop(self):
    self.running = False

  def setKey(self, key):
    self.key = key

if __name__ == "__main__":
  cans = {}
  def opener(id, ans):
    if id not in cans:
      return
    if ans == "quit":
      cans[id].stop()  
  c = Can(1, opener, "non-real")
  cans[c.id] = c
  c.start()
