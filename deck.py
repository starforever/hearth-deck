from cStringIO import StringIO
import time
from cPickle import loads as pickle_loads
from card_info import card_by_id

class Deck ():

  @classmethod
  def from_database (cls, row):
    if row is None:
      return None
    deck = Deck()
    deck.id = row['id']
    deck.name = row['name']
    deck.author = row['author']
    deck.url = row['url']
    deck.type = row['type']
    deck.hero_class = row['class']
    deck.dust_cost = row['dust_cost']
    deck.rating = row['rating']
    deck.num_view = row['num_view']
    deck.num_comment = row['num_comment']
    deck.time_update = time.localtime(row['time_update'])
    deck.cards = pickle_loads(str(row['cards']))
    deck.scan_count = row['scan_count']
    return deck

  def is_valid (self):
    total = 0
    for (id, count) in self.cards:
      total += count
      card = card_by_id(id)
      if card.hero_class == '' or card.set == 'Discarded':
        return False
    return total == 30

  def __str__ (self):
    ss = StringIO()
    ss.write('%s (by %s)\n' % (self.name.encode('utf-8'), self.author.encode('utf-8')))
    ss.write('URL: %s (%d)\n' % (self.url, self.id))
    ss.write('Type: %s, Class: %s, Cost: %d\n' % (self.type, self.hero_class, self.dust_cost))
    ss.write('Rating: %d, Views: %d, Comments: %d\n' % (self.rating, self.num_view, self.num_comment))
    ss.write('Updated: %s\n' % time.strftime('%Y-%m-%d %H:%M:%S', self.time_update))
    ss.write('Cards:\n%s\n' % '\n'.join(['  %s x %d' % (card_by_id(c[0]).name, c[1]) for c in self.cards]))
    ss.write('Scan count: %d\n' % self.scan_count)
    ss.write('\n')
    return ss.getvalue()
