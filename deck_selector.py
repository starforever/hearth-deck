from cStringIO import StringIO
import time
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

def split_card (deck):
  card_hand = []
  card_forge = []
  card_soul = []
  cost_total = 0
  for (id, needed) in deck.cards:
    card = card_by_id(id)
    available = COLLECTION[id] if id in COLLECTION else 0
    if available > 0:
      card_hand.append((card, min(needed, available)))
    if needed > available:
      if card.can_be_forged():
        card_forge.append((card, needed - available))
        cost_total += card.forge_cost() * (needed - available)
      else:
        card_soul.append((card, needed - available))
  return (card_hand, card_forge, card_soul, cost_total)

def show_deck (deck, cost_total, card_hand, card_forge, card_soul):
  print '%s (by %s)' % (deck.name, deck.author)
  print 'Rating: %d, Type: %s, Updated: %s' % (deck.rating, deck.type, time.strftime('%Y-%m-%d %H:%M:%S', deck.time_update))
  if card_hand:
    print 'Cards already in your collection:'
    print '\n'.join(['  %s x %d' % (card.colored_name(), count) for (card, count) in card_hand])
  if card_forge:
    print 'Cards can be forged:'
    print '\n'.join(['  %s x %d' % (card.colored_name(), count) for (card, count) in card_forge])
    print '  Total Arcane Dust: %d' % cost_total
  if card_soul:
    print 'Cards can not be forged (Soulbound):'
    print '\n'.join(['  %s x %d' % (card.colored_name(), count) for (card, count) in card_soul])
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
      (card_hand, card_forge, card_soul, cost_total) = split_card(deck)
      if not card_soul and cost_total <= dust_amount or dust_amount == -1:
        show_deck(deck, cost_total, card_hand, card_forge, card_soul)
        if raw_input('Press Enter to continue. Input (X) and enter to exit.\n').upper() == 'X':
          break
  database_close()
