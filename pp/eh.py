####    command-line arguments
# sys.argv is used to get the command line arguments

import sys
#try:
 
if len(sys.argv) < 2:
    sys.exit("Too few arguments provided")
#elif len(sys.argv) > 2:
  #  sys.exit("Too many arguments provided")
#else:
 #   print("hello, my name is", sys.argv[1])

for arg in sys.argv[1:]:
   print("hello, my name is", arg)