class Deck ():
  def __str__ (self):
    return '%s (by %s)\nType: %s\nClass: %s\nRating: %d\nViews: %d\nComments: %d\nCost: %d\nUpdated: %s\n' % (self.name.encode('utf-8'), self.author.encode('utf-8'), self.type, self.hclass, self.rating, self.num_view, self.num_comment, self.dust_cost, self.time_update)
