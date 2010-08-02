
from threading import Thread
import BaseHTTPServer
import urllib

instants = None
class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_GET(self):
    msg = ""
    if self.path: 
      msg = urllib.unquote(self.path[1:])
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    r = "<HTML>"
    r += "<BODY>"
    r += "Msg Sent: %s" % msg
    r += "</BODY>"
    r += "</HTML>"
    self.wfile.write(r)
    if msg:
      global instants
      instants.answer(msg)
    return


class Can(Thread):
  def __init__(self, id, config, opener, key):
    Thread.__init__(self)
    self.key = key
    self.config = config
    self.id = id
    self.opener = opener
    self.running = True
    global instants
    instants = self

  def answer(self, ans):
    self.opener(self.id, ans)

  def run(self):
    server_class = BaseHTTPServer.HTTPServer
    self.httpd = server_class(("", 8088), Handler)
    while self.running:
      self.httpd.handle_request()
    self.httpd.server_close()

  def stop(self):
    self.running = False
    self.httpd.server_close()

  def setKey(self, key):
    self.key = key


if __name__ == "__main__":
  cans = {}
  def opener(id, ans):
    if id not in cans:
      return
    print ans
    if "q" in ans:
      print "stopped"
      cans[id].stop()  
  c = Can(1, opener, "non-real")
  cans[c.id] = c
  c.start()
  print "started"
  c.join()
  print "done"
