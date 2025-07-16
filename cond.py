# Conditionals: forks on roads
### symbols:
#### > >= < <= == !=

x = int(input("What's X? "))
y = int(input("What's Y? "))

if x < y:
    print("X is less than Y")
elif x > y:
    print("X is greater than Y")
else:
    print("X is equal to Y")

if x < y or x > y:
    print("X is not equal to Y")
else:
    print("X is equal to Y")