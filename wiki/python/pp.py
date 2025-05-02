call = input("Name: ")
print(f"Hello, {call}")

n = int(input("Your age is: "))
if n > 21:
    print(f"{call}, start making your will, you oldie")
elif n < 21:
    print(f"{call}, you were born like yesterday LOL")
else:
    print(f"{call}, sweetie, you are just fine.")
print(f"Your name starts with {call[0]}")

#Practising with list and conditions
names = ["Tomoyo", "Laurie", "Sakura"]
choice = int(input("chose your favorite name from 0 to 2: "))
while choice != 0 and choice >= 3:
    choice = int(input("chose your favorite name from 0 to 2: "))
print(f"Your child will be called {names[choice]}")

# Practicing with looping
for name in names:
    print(name)

# Practising with Dictionaries
richor = {"Tomoyo": "super Rich", "Laurie": "rich", "Sakura": "middle Class"}

print("Your kid's name's spelled:")
for character in names[choice]:
    print(character)

print(f"You've chosen {names[choice]}, which means that you both are gonna be {richor[names[choice]]}")
      