#name = input("Name: ")
#print("Hello, " + name + "!")
#print(f"Hello, {name}!")

n = int(input("Number: "))
# This throws a TypeError, as if you try to compare a string with an integer.
### TypeError: the types of values involved are not compatible
# To fix, turn the input into an integer. 
if n > 0:
    print("Positive")