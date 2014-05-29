from cStringIO import StringIO
from cardid import get_card_name

class Deck ():
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
