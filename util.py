import sys

def parse_arg (arg_types, num_required):
  if len(sys.argv) < num_required + 1:
    print >> sys.stderr, 'Not enough arguments'
    sys.exit(1)
  argv = []
  for i in range(len(arg_types)):
    argv.append(arg_types[i](sys.argv[i + 1]) if i + 1 < len(sys.argv) else None)
  return argv
