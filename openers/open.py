import webbrowser

class Opener():
  def __init__(self, id, config):
    self.id = id
    self.config = config

  def match(self, name):
    return name == "open"

  def open(self, params):
    webbrowser.open(params)
