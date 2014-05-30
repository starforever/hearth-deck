def init (filename):
  global CARD_ID
  global CARD_NAME
  print 'Loading card id mapping from %s' % filename
  CARD_ID = {}
  CARD_NAME = []
  cid = 0
  fin = open(filename, 'r')
  while True:
    line = fin.readline()
    if not line:
      break
    line = line[:-1]
    names = line.split(';')
    CARD_NAME.append(names[0])
    for name in names:
      if name in CARD_ID:
        raise Exception('Duplicate card names: %s' % name)
      CARD_ID[name] = cid
    cid += 1
  fin.close()

def get_id (name):
  return CARD_ID[name]

def get_name (id):
  return CARD_NAME[id]

init('cardid.txt')
