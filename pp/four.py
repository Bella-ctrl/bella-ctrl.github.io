#import random """WITH THIS YOU IMPORT EVERYTHING

#coin = random.choice(["heads", "tails"])
#print("The coin landed on:", coin)

from random import choice  # Only import the choice function

coin = choice(["heads", "tails"])
print("The coin landed on:", coin)