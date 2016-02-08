from termcolor import colored

class Card ():

  FORGE_COST = {'Legendary': 1600, 'Epic': 400, 'Rare': 100, 'Common': 40, 'Free': 0}
  DUST_VALUE = {'Legendary': 400, 'Epic': 100, 'Rare': 20, 'Common': 5, 'Free': 0}
  COLOR = {'Legendary': 'red', 'Epic': 'magenta', 'Rare': 'blue', 'Common': 'green', 'Free': 'white'}
  SET_FORGE = ['Classic', 'Promotion', 'Goblins vs Gnomes', 'The Grand Tournament']
  SET_PURCHASE = ['Classic', 'Goblins vs Gnomes', 'The Grand Tournament']

  @classmethod
  def from_csv (cls, row):
    card = Card()
    card.id = int(row['id'])
    card.name = row['name']
    card.type = row['type']
    card.hero_class = row['class']
    card.set = row['set']
    card.rarity = row['rarity']
    card.race = row['race']
    card.cost = int(row['cost'])
    if card.type in ['Minion', 'Weapon']:
      card.attack = int(row['attack'])
      card.health = int(row['health'])
    else:
      card.attack = 0
      card.health = 0
    card.power = row['power']
    return card

  def can_be_collected (self):
    return self.hero_class != '' and self.set != 'Discarded'

  def can_be_forged (self):
    return self.hero_class != '' and self.set in SET_FORGE

  def forge_cost (self):
    if self.rarity not in Card.FORGE_COST:
      raise Exception('Incorrect rarity for card: %s [%s]' % (self.name, self.rarity))
    else:
      return Card.FORGE_COST[self.rarity]

  def dust_value (self):
    if self.rarity not in Card.DUST_VALUE:
      raise Exception('Incorrect rarity for card: %s [%s]' % (self.name, self.rarity))
    else:
      return Card.DUST_VALUE[self.rarity]

  def colored_name (self):
    if self.rarity not in Card.COLOR:
      raise Exception('Incorrect rarity for card: %s [%s]' % (self.name, self.rarity))
    return colored(self.name, Card.COLOR[self.rarity], attrs=['bold'])

  def __str__ (self):
    ss = StringIO()
    ss.write('%s (%d)\n' % (self.name, self.id))
    ss.write('Type: %s, Class: %s, Set: %s, Rarity: %s' % (self.type, self.hero_class, self.set, self.rarity))
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
