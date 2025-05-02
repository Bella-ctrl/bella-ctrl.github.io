name = input("Name: ")
print(f"Hello, {name}")

n = int(input("Your age is: "))
if n > 21:
    print(f"{name}, start making your will, you oldie")
elif n < 21:
    print(f"{name}, you were born like yesterday LOL")

print(f"Your name starts with {name[0]}")

names = ["Tomoyo", "Laurie", "Sakura"]
choice = int(input("chose your favorite name from 0 to 2: "))
while choice != 0 and choice >= 3:
    choice = int(input("chose your favorite name from 0 to 2: "))
print(f"Your child will be called {names[choice]}")
