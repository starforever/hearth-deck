def load (filename):
  global CARD_ID
  print 'Loading card id mapping from %s' % filename
  CARD_ID = {}
  cid = 0
  fin = open(filename, 'r')
  while True:
    line = fin.readline()
    if not line:
      break
    line = line[:-1]
    cid += 1
    for name in line.split(';'):
      if name in CARD_ID:
        raise Exception('Duplicate card names: %s' % name)
      CARD_ID[name] = cid
  fin.close()

def get_id (name):
  return CARD_ID[name]

load('cardid.txt')
