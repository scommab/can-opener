
import random
import sys
import cans as cans_module
cans = {}

def opener(id, ans):
  if id not in cans:
# this shouldn't happen
    return
  if ans == "q":
    for c in cans.values():
      c.stop()
    sys.exit()



key = random.randint(1, sys.maxint)
print key

can_count = 0
for a in dir(cans_module):
  if a.startswith("__"):
    continue
  print "Starting can %s" % a
  mod = getattr(cans_module, a)
  if not hasattr(mod, "Can"):
    continue
  cans[can_count] = getattr(cans_module, a).Can(can_count, opener, key)
  cans[can_count].start()
  can_count += 1
