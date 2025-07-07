#name = input("Name: ")
#print("Hello, " + name + "!")
#print(f"Hello, {name}!")

n = int(input("Number: "))
# This throws a TypeError - To fix, turn the input into an integer.
### TypeError: the types of values involved are not compatible 
if n > 0:
    print("Positive")
elif n < 0:
    print("Negative")
else:
    print("Zero")