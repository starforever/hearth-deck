import time
import re
import lxml.html
from util import parse_arg
from deck import Deck
from database_op import database_connect, database_close, database_commit, database_rollback, deck_create, deck_insert, deck_find_by_id, deck_remove_unscanned
from card_info import card_by_name
from key_store import save as save_key, load as load_key

REST_INTERVAL = 3
DOMAIN = 'http://www.hearthpwn.com'

DUST_COST_MATCHER = re.compile('.*Crafting Cost: -?(\d+).*', re.DOTALL)
DECK_ID_MATCHER = re.compile('/decks/(\d+).*')
CARD_COUNT_MATCHER = re.compile(u'.*\xd7 -?(\d+).*', re.DOTALL)

DECK_BUFFER_SIZE = 64;

def get_page_root (url):
  root = None
  while root is None:
    try:
      root = lxml.html.parse(url).getroot()
    except IOError as e:
      print e
      print 'Retry after %d seconds.' % REST_INTERVAL
      time.sleep(REST_INTERVAL)
  return root

def parse_row (row):
  deck = Deck()
  deck.url = row.find_class('col-name')[0].xpath('div/span/a')[0].attrib['href']
  deck.id = int(DECK_ID_MATCHER.match(deck.url).groups()[0])
  deck.name = row.find_class('col-name')[0].xpath('div/span/a')[0].text_content()
  deck.author = row.find_class('col-name')[0].xpath('div/small/a')[0].text_content()
  deck.type = row.find_class('col-deck-type')[0].text_content()
  deck.hero_class = row.find_class('col-class')[0].text_content()
  deck.rating = int(row.find_class('col-ratings')[0].xpath('div')[0].text_content())
  deck.num_view = int(row.find_class('col-views')[0].text_content())
  deck.num_comment = int(row.find_class('col-comments')[0].text_content())
  deck.time_update = time.localtime(int(row.find_class('col-updated')[0].xpath('abbr')[0].attrib['data-epoch']))
  deck.scan_count = SCAN_COUNT
  return deck

def parse_deck (deck):
  url = DOMAIN + deck.url
  while True:
      try:
        root = get_page_root(url)
        deck.dust_cost = int(root.find_class('craft-cost')[0].text_content())
        info = root.find_class('infobox')[0]
        rows = []
        for sec in info.find_class('t-deck-details-card-list'):
          if sec.find_class('listing'):
            rows.extend(sec.find_class('listing')[0].xpath('tbody/tr'))
        deck.cards = []
        for row in rows:
          name = row.find_class('col-name')[0].xpath('b/a')[0].text_content()
          count = int(CARD_COUNT_MATCHER.match(row.find_class('col-name')[0].text_content()).groups()[0])
          deck.cards.append((card_by_name(name).id, count))
        return
      except (IndexError, KeyError) as e:
        print e
        print 'Retry after %d seconds.' % REST_INTERVAL
        time.sleep(REST_INTERVAL)

def process_deck (deck):
  old_deck = Deck.from_database(deck_find_by_id(deck.id))
  if old_deck is not None and deck.time_update == old_deck.time_update:
    deck.dust_cost = old_deck.dust_cost
    deck.cards = old_deck.cards
    status = 'Pass'
  else:
    parse_deck(deck)
    status = 'Update' if old_deck is not None else 'New'
  if not deck.is_valid():
    status += ', Invalid'
  return status

def parse_page (pagenum, rownum):
  global DECK_BUFFER_NUM
  print '(%s) Parsing page %d...' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), pagenum)
  url = DOMAIN + '/decks?filter-is-forge=2&sort=-datemodified&page=%d' % pagenum
  root = get_page_root(url)
  rows = root.get_element_by_id('decks').xpath('tbody/tr')
  while rownum < len(rows):
    deck = parse_row(rows[rownum])
    status = process_deck(deck)
    deck_insert(deck)
    DECK_BUFFER_NUM += 1
    rownum += 1
    print '  [%d] (%s) %s' % (deck.id, status, deck.name)
    if DECK_BUFFER_NUM >= DECK_BUFFER_SIZE:
      database_commit()
      DECK_BUFFER_NUM = 0
      save_key('CURRENT_PAGE', pagenum)
      save_key('CURRENT_ROW', rownum)
  has_next = 'Next' in [e.text_content() for e in root.find_class('paging-list')[0].xpath('li/a')]
  return has_next

def parse ():
  global DECK_BUFFER_NUM, SCAN_COUNT
  while True:
    try:
      DECK_BUFFER_NUM = 0
      SCAN_COUNT = load_key('SCAN_COUNT', 1)
      pagenum = load_key('CURRENT_PAGE', 1)
      rownum = load_key('CURRENT_ROW', 0)
      while parse_page(pagenum, rownum):
        pagenum += 1
        rownum = 0
      deck_remove_unscanned(SCAN_COUNT)
      break
    except (IndexError, KeyError) as e:
      database_rollback()
      print e
      print 'Retry after %d seconds.' % REST_INTERVAL
      time.sleep(REST_INTERVAL)
  database_commit()
  SCAN_COUNT += 1
  save_key('SCAN_COUNT', SCAN_COUNT)
  save_key('CURRENT_PAGE', 1)
  save_key('CURRENT_ROW', 0)
  print 'Scan pass %d finished!' % (SCAN_COUNT - 1)

if __name__ == '__main__':
  (database_name,) = parse_arg((str,), 1)
  database_connect(database_name)
  deck_create()
  parse()
  database_close()
