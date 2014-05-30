import os.path
import cPickle

def init (filename):
  global STORE
  global STORE_FILE
  STORE_FILE = filename
  if os.path.isfile(filename):
    STORE = cPickle.load(open(filename, 'rb'))
  else:
    STORE = {}

def save (key, value):
  STORE[key] = value
  commit()

def load (key, default = None):
  if key in STORE:
    return STORE[key]
  else:
    return default

def clear ():
  STORE.clear()
  commit()

def commit ():
  cPickle.dump(STORE, open(STORE_FILE, 'wb'), -1)

init('key_store')
