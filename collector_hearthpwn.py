import datetime
import lxml.html
from model import Deck
from database_op import database_connect

# REST_INTERVAL = 3
DOMAIN = 'http://www.hearthpwn.com'

def parse_page (pagenum):
  url = DOMAIN + '/decks?filter-is-forge=2&sort=-datemodified&page=%d' % pagenum
  root = lxml.html.parse(url).getroot()
  decks = root.get_element_by_id('decks').xpath('tbody/tr')
  for row in decks:
    deck = Deck()
    deck.url = row.find_class('col-name')[0].xpath('div/span/a')[0].attrib['href']
    deck.name = row.find_class('col-name')[0].xpath('div/span/a')[0].text_content()
    deck.author = row.find_class('col-name')[0].xpath('div/small/a')[0].text_content()
    deck.type = row.find_class('col-deck-type')[0].text_content()
    deck.hclass = row.find_class('col-class')[0].text_content()
    deck.rating = int(row.find_class('col-ratings')[0].xpath('div')[0].text_content())
    deck.num_view = int(row.find_class('col-views')[0].text_content())
    deck.num_comment = int(row.find_class('col-comments')[0].text_content())
    deck.dust_cost = 0
    deck.time_update = datetime.datetime.fromtimestamp(int(row.find_class('col-updated')[0].xpath('abbr')[0].attrib['data-epoch']))
    print deck

if __name__ == '__main__':
  # database_name = parse_arg((str), 1)
  # database_connect(database_name)
  parse_page(1)
  # database_close()
