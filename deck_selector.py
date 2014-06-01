from cStringIO import StringIO
import re
from util import parse_arg
from deck import Deck
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
  elif card.rarity == 'Basic':
    return 1000000 # Basic cards cannot be forged
  else:
    raise Exception('Incorrect rarity for card: %s' % card.name)

def deck_forge_cost (deck):
  cost = 0
  for (id, count) in deck.cards:
    card = card_by_id(id)
    available = COLLECTION[id] if id in COLLECTION else 0
    if count > available:
      cost += card_forge_cost(card) * (count - available)
  return cost

def show_deck (deck):
  print '%s (by %s)' % (deck.name.encode('utf-8'), deck.author.encode('utf-8'))
  print 'Rating: %d, Type: %s' % (deck.rating, deck.type)
  card_hand = []
  card_craft = []
  for (id, count) in deck.cards:
    card = card_by_id(id)
    available = COLLECTION[id] if id in COLLECTION else 0
    if available > 0:
      card_hand.append((card, min(count, available)))
    if count > available:
      card_craft.append((card, count - available))
  print 'Cards already in your hand:'
  print '\n'.join(['  %s x %d' % (card.name, count) for (card, count) in card_hand])
  if card_craft:
    print 'Cards need crafting:'
    total = 0
    for (card, count) in card_craft:
      cost = card_forge_cost(card) * count
      total += cost
      print '  %s x %d ($%d)' % (card.name, count, cost)
    print '  Total: $%d' % total
  print

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
      if raw_input('Press Enter to continue. Input (X) and enter to exit.\n').upper() == 'X':
        break
  database_close()
