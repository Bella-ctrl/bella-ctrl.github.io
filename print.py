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



# Data structures
## Dict - collection of key-value pairs
houses = {"Harry": "Gryffindor", "Draco": "Slytherin"}
print(houses["Harry"])  # Gryffindor
houses["Hermione"] = "Gryffindor"  # Adding a new key-value pair
print(houses)  # {'Harry': 'Gryffindor', 'Draco': 'Slytherin', 'Hermione': 'Gryffindor'}


## List - seq of mutable values
names = ["Harry", "Ron", "Hermione"]
###print(names[0])  # Harry
names.append("Draco")  # Adding a new name
names.sort()  # Sorting the list
###print(names)  # ['Draco', 'Harry', 'Hermione', 'Ron']

## Tuple - seq of immutable values
###point = (10, 20)
###print(point[0]) # 10
###print(point[1]) # 20

## Set - collection of unique values that are unordered
###s = set()
###s.add(1)  # Adding a number
###s.add(2)  # Adding another number
###s.add(1)  # Adding a duplicate number (no effect)
###print(s)  # {1, 2}
###s.remove(1)  # Removing a number
###print(s)  # {2}

###fruits = {"apple", "banana", "cherry"}
###fruits.add("orange")  # Adding a new fruit




# Loops
for i in [0, 1, 2, 3, 4]:
    print(i)  # Prints numbers from 0 to 4

for i in range(5):  # Generates numbers from 0 to 4
    print(i)  # Prints numbers from 0 to 4

