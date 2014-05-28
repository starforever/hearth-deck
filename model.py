class Deck ():
  def __str__ (self):
    return '%s (by %s)\nURL: %s\nType: %s\nClass: %s\nRating: %d\nViews: %d\nComments: %d\nCost: %d\nUpdated: %s\nCards:\n%s\n' % (self.name.encode('utf-8'), self.author.encode('utf-8'), self.url, self.type, self.hclass, self.rating, self.num_view, self.num_comment, self.dust_cost, self.time_update, '\n'.join(self.cards))
