####    command-line arguments
# sys.argv is used to get the command line arguments

import sys
#try:
 
if len(sys.argv) < 2:
    print("Usage: python eh.py <name>")
elif len(sys.argv) > 2:
    print("Too many arguments provided")
else:
    print("hello, my name is", sys.argv[1])