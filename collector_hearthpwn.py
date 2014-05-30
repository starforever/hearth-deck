import datetime
import re
import lxml.html
from util import parse_arg
from model import Deck
from database_op import database_connect, database_close, deck_create, deck_insert, deck_select
from card_id import get_card_id

# REST_INTERVAL = 3
DOMAIN = 'http://www.hearthpwn.com'

DUST_COST_MATCHER = re.compile('.*Crafting Cost: (\d+).*', re.DOTALL)
DECK_ID_MATCHER = re.compile('/decks/(\d+)-.*')
CARD_COUNT_MATCHER = re.compile(u'.*\xd7 (\d+).*', re.DOTALL)

def parse_deck (deck):
  url = DOMAIN + deck.url
  info = lxml.html.parse(url).getroot().find_class('infobox')[0]
  deck.dust_cost = int(DUST_COST_MATCHER.match(info.find_class('t-deck-dust-cost')[0].text_content()).groups()[0])
  rows = []
  for sec in info.find_class('t-deck-details-card-list'):
    rows.extend(sec.find_class('listing')[0].xpath('tbody/tr'))
  deck.cards = []
  for row in rows:
    name = row.find_class('col-name')[0].xpath('b/a')[0].text_content()
    count = int(CARD_COUNT_MATCHER.match(row.find_class('col-name')[0].text_content()).groups()[0])
    deck.cards.append((get_card_id(name), count))

def parse_page (pagenum):
  url = DOMAIN + '/decks?filter-is-forge=2&sort=-datemodified&page=%d' % pagenum
  root = lxml.html.parse(url).getroot()
  rows = root.get_element_by_id('decks').xpath('tbody/tr')
  for row in rows:
    deck = Deck()
    deck.url = row.find_class('col-name')[0].xpath('div/span/a')[0].attrib['href']
    deck.source = 'HearthPwn'
    deck.source_id = int(DECK_ID_MATCHER.match(deck.url).groups()[0])
    deck.name = row.find_class('col-name')[0].xpath('div/span/a')[0].text_content()
    deck.author = row.find_class('col-name')[0].xpath('div/small/a')[0].text_content()
    deck.type = row.find_class('col-deck-type')[0].text_content()
    deck.hclass = row.find_class('col-class')[0].text_content()
    deck.rating = int(row.find_class('col-ratings')[0].xpath('div')[0].text_content())
    deck.num_view = int(row.find_class('col-views')[0].text_content())
    deck.num_comment = int(row.find_class('col-comments')[0].text_content())
    deck.time_update = datetime.datetime.fromtimestamp(int(row.find_class('col-updated')[0].xpath('abbr')[0].attrib['data-epoch']))
    parse_deck(deck)
    deck_insert(deck)
    break

def print_decks ():
  for row in deck_select():
    deck = Deck.from_database(row)
    print deck

if __name__ == '__main__':
  (database_name,) = parse_arg((str,), 1)
  database_connect(database_name)
  deck_create()
  parse_page(1)
  print_decks()
  database_close()
