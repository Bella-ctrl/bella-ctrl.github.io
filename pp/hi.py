try:
    x = int(input("What's x? "))
    print(f"x is {x}")
except ValueError:
    print("Invalid input. Please enter a number.")