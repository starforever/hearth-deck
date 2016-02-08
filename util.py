import sys
import random

def dict2list (dct, key_map):
  lst = [None] * len(dct)
  for k in dct:
    lst[key_map[k]] = dct[k]
  return lst

def parse_arg (arg_types, num_required):
  if len(sys.argv) < num_required + 1:
    print >> sys.stderr, 'Not enough arguments'
    sys.exit(1)
  argv = []
  for i in range(len(arg_types)):
    argv.append(arg_types[i](sys.argv[i + 1]) if i + 1 < len(sys.argv) else None)
  return argv

def random_spin (probability):
  x = random.random() * sum(probability);
  sm = 0.0
  i = 0
  while i < len(probability) and x >= sm:
    sm += probability[i]
    i += 1
  return i - 1
