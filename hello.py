print("hello, world")
name = input("What is your name? ").strip().title()
print("Hello, " + name)

# Split user's name into first and last name
first, last = name.split(" ")

print(f"Hello, {first}", "again!")