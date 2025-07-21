print("hello, world")
name = input("What is your name? ").strip().title()
print("Hello, " + name)

# Split user's name into first and last name
first, last = name.split(" ")

print(f"Hello, {first}", "again!")

x = int(input("Enter a number: "))
y = int(input("Enter another number: "))

print(f"The sum of {x} and {y} is {(x) + (y)}")

m = int(input("Enter a number: "))
if m % 2 == 0:
    print(f"{m} is even")
else:
    print(f"{m} is odd")

n = int(input("Enter a number: "))
print(f"The numbered entered is {n:,}")
print(f"The number entered is {n:.2f}")

