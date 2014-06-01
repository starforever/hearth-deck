class Card ():

  @classmethod
  def from_csv (cls, row):
    card = Card()
    card.id = int(row['id'])
    card.name = row['name']
    card.type = row['type']
    card.hero_class = row['class']
    card.race = row['race']
    card.rarity = row['rarity']
    card.cost = int(row['cost'])
    if card.type in ['Minion', 'Weapon']:
      card.attack = int(row['attack'])
      card.health = int(row['health'])
    else:
      card.attack = 0
      card.health = 0
    card.power = row['power']
    return card

  def __str__ (self):
    ss = StringIO()
    ss.write('%s (%d)\n' % (self.name, self.id))
    ss.write('Type: %s, Class: %s, Rarity: %s' % (self.type, self.hero_class, self.rarity))
    if self.race:
      ss.write(', Race: %s' % self.race)
    ss.write('\n')
    ss.write('Cost: %d' % self.cost)
    if self.type in ['Minion', 'Weapon']:
      ss.write(', Attack: %d, %s: %d' % (self.attack, 'Health' if self.type == 'Minion' else 'Durability', self.health))
    ss.write('\n')
    if self.power:
      ss.write('%s\n' % self.power)
    ss.write('\n')
    return ss.getvalue()
