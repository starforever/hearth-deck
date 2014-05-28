class Deck ():
  def __str__ (self):
    return '%s (by %s)\nURL: %s (%d)\nType: %s, Class: %s, Cost: %d\nRating: %d, Views: %d, Comments: %d\nUpdated: %s\nCards:\n%s\n' % (self.name.encode('utf-8'), self.author.encode('utf-8'), self.url, self.id, self.type, self.hclass, self.dust_cost, self.rating, self.num_view, self.num_comment, self.time_update, '\n'.join(self.cards))
