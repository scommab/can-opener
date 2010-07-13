
import random
import sys
import cans as cans_module
cans = {}

running = True
def opener(id, ans):
  print "opener(%s, \"%s\")" % (id, ans)
  if id not in cans:
# this shouldn't happen
    return
  if ans == "quit":
    print "quiting"
    global running
    running = False

key = random.randint(1, sys.maxint)
print key

for a in dir(cans_module):
  if a.startswith("__"):
    continue
  mod = getattr(cans_module, a)
  if not hasattr(mod, "Can"):
    continue
  print 'Starting can "%s"' % a
  cans[a] = getattr(cans_module, a).Can(a, opener, key)
  cans[a].start()

while running:
  pass

keys = cans.keys()
for k in keys:
  print 'Stopping "%s"' % k
  cans[k].stop()
  cans[k].join()
  print "Stoped"
