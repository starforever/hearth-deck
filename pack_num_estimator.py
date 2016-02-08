import copy
import math
import re
import sys
from card import Card
from card_info import card_by_name, all_cards
from util import dict2list, parse_arg, random_spin

CARD_PER_PACK = 5
CARD_MATCHER = re.compile('(.+?)(?: x (\d+))?\Z')
RARITY_CODE = {'Legendary': 0, 'Epic': 1, 'Rare': 2, 'Common': 3, 'Free': 4}
DRAW_PERCENT = [0.0110, 0.0442, 0.2284, 0.7165]

def init_global ():
  global FORGE_COST
  global DUST_VALUE
  FORGE_COST = dict2list(Card.FORGE_COST, RARITY_CODE)
  DUST_VALUE = dict2list(Card.DUST_VALUE, RARITY_CODE)

def count_card_collection (filename, card_set):
  card_count = [[0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
  for card in all_cards():
    if card.set == card_set and card.can_be_collected():
      card_count[RARITY_CODE[card.rarity]][0] += 1
  fin = open(filename, 'r')
  for line in fin:
    line = line[:-1]
    groups = CARD_MATCHER.match(line).groups()
    name = groups[0]
    count = int(groups[1]) if groups[1] is not None else 1
    card = card_by_name(name)
    if card.set == card_set:
      card_count[RARITY_CODE[card.rarity]][0] -= 1
      card_count[RARITY_CODE[card.rarity]][count] += 1
  fin.close()
  return card_count

def calc_required_dust (card_count):
  required_dust = 0
  for rarity in range(len(card_count)):
    for count in range(len(card_count[rarity]) - 1):
      required_dust += FORGE_COST[rarity] * (len(card_count[rarity]) - 1 - count) * card_count[rarity][count]
  return required_dust

def draw_card (card_count):
  rarity = random_spin(DRAW_PERCENT)
  count = random_spin(card_count[rarity])
  return (rarity, count)

def simulate_draw (card_count, curr_dust, required_dust):
  num_draw = 0
  while curr_dust < required_dust:
    (rarity, count) = draw_card(card_count)
    num_draw += 1
    if count + 1 < len(card_count[rarity]):
      card_count[rarity][count] -= 1
      card_count[rarity][count + 1] += 1
      required_dust -= FORGE_COST[rarity]
    else:
      curr_dust += DUST_VALUE[rarity]
  return num_draw

def estimate_pack_num (card_count, curr_dust, required_dust, simulate_num):
  ave_draw = 0.0
  simulate_round = 0
  while simulate_round < simulate_num:
    card_count_copy = copy.deepcopy(card_count)
    ave_draw += simulate_draw(card_count_copy, curr_dust, required_dust)
    simulate_round += 1
  ave_draw /= simulate_num
  return int(math.ceil(round(ave_draw) / CARD_PER_PACK))

if __name__ == '__main__':
  (collection_name, card_set, dust_amount, simulate_num) = parse_arg((str, str, int, int), 2)
  if card_set not in Card.SET_PURCHASE:
    print '%s is not available to purchase in Shop.' % card_set
    sys.exit(1)
  if dust_amount is None:
    dust_amount = 0
  if simulate_num is None:
    simulate_num = 100
  init_global()
  card_count = count_card_collection(collection_name, card_set)
  required_dust = calc_required_dust(card_count)
  pack_num = estimate_pack_num(card_count, dust_amount, required_dust, simulate_num)
  print 'The estimated number of packs to purchase for set %s is %d.' % (card_set, pack_num)
