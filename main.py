
import random
import sys
import cans as cans_module
import openers as openers_module
import ConfigParser
cans = {}
openers = {}

running = True
def opener(id, ans):
  print "opener(%s, \"%s\")" % (id, ans)
  if id not in cans:
    # this shouldn't happen
    return
  values = ans.split(" ")
  if len(values) == 0:
    return
  action = values[0]
  params = " ".join(values[1:])
  if action == "quit":
    print "quiting"
    global running
    running = False
    return
  for opener in openers.values():
    if opener.match(action):
      opener.open(params)
  #elif action == "open" and len(values) > 1:
  #  print " ".join(values[1:])

config = ConfigParser.RawConfigParser()
config.read('can-opener.cfg')

key = random.randint(1, sys.maxint)
print key

for a in dir(cans_module):
  if a.startswith("__"):
    continue
  mod = getattr(cans_module, a)
  if not hasattr(mod, "Can"):
    continue
  print 'Starting can "%s"' % a
  cans[a] = getattr(cans_module, a).Can(a, config, opener, key)
  cans[a].daemon = True
  cans[a].start()

for a in dir(openers_module):
  if a.startswith("__"):
    continue
  mod = getattr(openers_module, a)
  if not hasattr(mod, "Opener"):
    continue
  print 'Loading opener "%s"' % a
  openers[a] = getattr(openers_module, a).Opener(a, config)

while running:
  pass

keys = cans.keys()
for k in keys:
  print 'Stopping "%s"' % k
  cans[k].stop()
  print "Stoped"
