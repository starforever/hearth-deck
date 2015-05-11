import time
import sqlite3
from cPickle import dumps as pickle_dumps

def database_connect (filename):
  global CONN
  CONN = sqlite3.connect(filename)
  CONN.row_factory = sqlite3.Row
  CONN.text_factory = sqlite3.OptimizedUnicode

def database_close ():
  CONN.close()

def database_commit ():
  CONN.commit()

def database_rollback ():
  CONN.rollback()

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
    time_update INTEGER,
    cards BLOB,
    scan_count INTEGER
  )""")

def deck_insert (deck):
  CONN.execute("""INSERT OR REPLACE INTO decks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (deck.id, deck.name, deck.author, deck.url, deck.type, deck.hero_class, deck.dust_cost, deck.rating, deck.num_view, deck.num_comment, int(time.mktime(deck.time_update)), buffer(pickle_dumps(deck.cards, -1)), deck.scan_count))

def deck_find_by_id (id):
  return CONN.execute("""SELECT * FROM decks WHERE id = ?""", (id,)).fetchone()

def deck_select_by_class (hero_class):
  return CONN.execute("""SELECT * FROM decks WHERE class = ? ORDER BY rating DESC""", (hero_class,))

def deck_remove_unscanned (scan_count):
  CONN.execute("""DELETE FROM decks WHERE scan_count < ?""", (scan_count,))
