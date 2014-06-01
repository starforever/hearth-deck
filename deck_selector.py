import re
from util import parse_arg
from model import Deck
from database_op import database_connect, database_close, deck_select_by_class
from card_info import card_by_name, card_by_id

CARD_MATCHER = re.compile('(.+?)(?: x (\d+))?\Z')

def load_card_collection (filename):
  global COLLECTION
  COLLECTION = {}
  fin = open(filename, 'r')
  for line in fin:
    line = line[:-1]
    groups = CARD_MATCHER.match(line).groups()
    name = groups[0]
    count = int(groups[1]) if groups[1] is not None else 1
    COLLECTION[card_by_name(name).id] = count
  fin.close()

def card_forge_cost (card):
  if card.rarity == 'Legendary':
    return 1600
  elif card.rarity == 'Epic':
    return 400
  elif card.rarity == 'Rare':
    return 100
  elif card.rarity == 'Common':
    return 40
  else:
    print 'Warning: potential incorrect rarity for card: %s' % card.name
    return 0

def deck_forge_cost (deck):
  cost = 0
  for (id, count) in deck.cards:
    card = card_by_id(id)
    available = COLLECTION[id] if id in COLLECTION else 0
    if count > available:
      cost += card_forge_cost(card) * (count - available)
  return cost

def show_deck (deck):
  print deck

if __name__ == '__main__':
  (database_name, collection_name, hero_class, dust_amount) = parse_arg((str, str, str, int), 3)
  if dust_amount is None:
    dust_amount = 0
  load_card_collection(collection_name)
  database_connect(database_name)
  for row in deck_select_by_class(hero_class):
    deck = Deck.from_database(row)
    if deck.is_valid() and deck_forge_cost(deck) <= dust_amount:
      show_deck(deck)
      raw_input('Press any key to continue.')
      print '\n'
  database_close()
