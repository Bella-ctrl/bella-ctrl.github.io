#name = input("Name: ")
#print("Hello, " + name + "!")
#print(f"Hello, {name}!")

###########n = int(input("Number: "))
# This throws a TypeError - To fix, turn the input into an integer.
### TypeError: the types of values involved are not compatible 
#####if n > 0:
    #print("Positive")
#####elif n < 0:
    #print("Negative")
#####else:
    #print("Zero")



# String types
name = "Harry"
print(name[0]) # H

# List types
names = ["Harry", "Ron", "Hermione"]
print(names[0]) # Harry
print(names[1]) # Ron
print(names[2]) # Hermione

# Tuple types -  value pairs that cannot be changed
point = (10, 20)
print(point[0]) # 10
print(point[1]) # 20

# Data structures
## Dict - collection of key-value pairs
## List - seq of mutable values
## Tuple - seq of immutable values
## Set - collection of unique values that are unordered