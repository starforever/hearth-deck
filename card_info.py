from csv import DictReader
from card import Card

def load (filename):
  global CARD_BY_NAME
  global CARD_BY_ID
  CARD_BY_NAME = {}
  CARD_BY_ID = {}
  reader = DictReader(open(filename, 'r'), delimiter = '\t')
  for row in reader:
    card = Card.from_csv(row)
    if card.name not in CARD_BY_NAME:
      CARD_BY_NAME[card.name] = card
    if card.id in CARD_BY_ID:
      raise Exception('Duplicate card IDs: %d' % card.id)
    CARD_BY_ID[card.id] = card

def card_by_name (name):
  if name not in CARD_BY_NAME:
    raise Exception('Card with name %s not found' % name)
  return CARD_BY_NAME[name]

def card_by_id (id):
  if id not in CARD_BY_ID:
    raise Exception('Card with ID %d not found' % id)
  return CARD_BY_ID[id]

load('card_info.txt')
