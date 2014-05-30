import sqlite3
from cPickle import dumps as pickle_dumps

def database_connect (filename):
  global CONN
  CONN = sqlite3.connect(filename)
  CONN.row_factory = sqlite3.Row
  CONN.text_factory = sqlite3.OptimizedUnicode

def database_close ():
  CONN.close()

def deck_create ():
  CONN.execute("""CREATE TABLE IF NOT EXISTS decks (
    id INTEGER PRIMARY KEY,
    name TEXT,
    author TEXT,
    url TEXT,
    type TEXT,
    class TEXT,
    dust_cost INTEGER,
    rating INTEGER,
    num_view INTEGER,
    num_comment INTEGER,
    time_update TEXT,
    cards BLOB
  )""")
  CONN.commit()

def deck_insert (deck):
  CONN.execute("""INSERT INTO decks (id, name, author, url, type, class, dust_cost, rating, num_view, num_comment, time_update, cards) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (deck.id, deck.name, deck.author, deck.url, deck.type, deck.hclass, deck.dust_cost, deck.rating, deck.num_view, deck.num_comment, deck.time_update.strftime('%Y-%m-%d %H:%M:%S.000'), buffer(pickle_dumps(deck.cards, -1))))
  CONN.commit()

def deck_select ():
  return CONN.execute("""SELECT * FROM decks""")
