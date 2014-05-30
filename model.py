from datetime import datetime
from cStringIO import StringIO
from cPickle import loads as pickle_loads
from card_id import get_name as get_card_name

class Deck ():

  @classmethod
  def from_database (cls, row):
    deck = Deck()
    deck.id = row['id']
    deck.name = row['name']
    deck.author = row['author']
    deck.url = row['url']
    deck.type = row['type']
    deck.hclass = row['class']
    deck.dust_cost = row['dust_cost']
    deck.rating = row['rating']
    deck.num_view = row['num_view']
    deck.num_comment = row['num_comment']
    deck.time_update = datetime.strptime(row['time_update'], '%Y-%m-%d %H:%M:%S.000')
    deck.cards = pickle_loads(str(row['cards']))
    return deck

  def __str__ (self):
    ss = StringIO()
    ss.write('%s (by %s)\n' % (self.name.encode('utf-8'), self.author.encode('utf-8')))
    ss.write('URL: %s (%d)\n' % (self.url, self.id))
    ss.write('Type: %s, Class: %s, Cost: %d\n' % (self.type, self.hclass, self.dust_cost))
    ss.write('Rating: %d, Views: %d, Comments: %d\n' % (self.rating, self.num_view, self.num_comment))
    ss.write('Updated: %s\n' % self.time_update)
    ss.write('Cards:\n%s' % '\n'.join(['%s x %d' % (get_card_name(c[0]), c[1]) for c in self.cards]))
    ss.write('\n')
    return ss.getvalue()
