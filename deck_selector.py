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

def find_craft_card (deck):
  cost_total = 0
  card_hand = []
  card_craft = []
  for (id, needed) in deck.cards:
    card = card_by_id(id)
    available = COLLECTION[id] if id in COLLECTION else 0
    if available > 0:
      card_hand.append((card, min(needed, available)))
    if needed > available:
      cost_total += card.forge_cost() * (needed - available)
      card_craft.append((card, needed - available))
  return (cost_total, card_hand, card_craft)

def show_deck (deck, cost_total, card_hand, card_craft):
  print '%s (by %s)' % (deck.name, deck.author)
  print 'Rating: %d, Type: %s' % (deck.rating, deck.type)
  print 'Cards already in your hand:'
  print '\n'.join(['  %s x %d' % (card.name, count) for (card, count) in card_hand])
  if card_craft:
    print 'Cards need crafting:'
    print '\n'.join(['  %s x %d ($%d)' % (card.name, count, card.forge_cost() * count) for (card, count) in card_craft])
    print '  Total: $%d' % cost_total
  print

if __name__ == '__main__':
  (database_name, collection_name, hero_class, dust_amount) = parse_arg((str, str, str, int), 3)
  if dust_amount is None:
    dust_amount = 0
  load_card_collection(collection_name)
  database_connect(database_name)
  for row in deck_select_by_class(hero_class):
    deck = Deck.from_database(row)
    if deck.is_valid():
      (cost_total, card_hand, card_craft) = find_craft_card(deck)
      if cost_total <= dust_amount or dust_amount == -1:
        show_deck(deck, cost_total, card_hand, card_craft)
        if raw_input('Press Enter to continue. Input (X) and enter to exit.\n').upper() == 'X':
          break
  database_close()
