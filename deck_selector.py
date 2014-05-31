import re
from util import parse_arg
from card_id import get_id as get_card_id, get_name as get_card_name

CARD_MATCHER = re.compile('(.+?)(?: x (\d+))?\Z')

def load_card_collection (filename):
  collection = {}
  fin = open(filename, 'r')
  while True:
    line = fin.readline()
    if line == '':
      break
    line = line[:-1]
    groups = CARD_MATCHER.match(line).groups()
    name = groups[0]
    count = int(groups[1]) if groups[1] is not None else 1
    collection[get_card_id(name)] = count
  fin.close()
  for (name_id, count) in collection.items():
    print '%s x %d' % (get_card_name(name_id), count)

if __name__ == '__main__':
  (database_name, collection_name, hero_class, dust_amount) = parse_arg((str, str, str, int), 3)
  if dust_amount is None:
    dust_amount = 0
  load_card_collection(collection_name)
  # database_connect(database_name)
  # database_close()
