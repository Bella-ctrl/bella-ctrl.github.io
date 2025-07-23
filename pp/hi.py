try:
    x = int(input("What's x? "))
except ValueError:
    print("Invalid input. Please enter a number.")

print(f"x is {x}")