import sqlite3

def database_connect (filename):
  global CONN
  CONN = sqlite3.connect(filename)
  CONN.row_factory = sqlite3.Row

def database_close ():
  CONN.close()
