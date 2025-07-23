while True:
    try:
        x = int(input("What's x? "))
        # break could be here 
    except ValueError:
        print("Invalid input. Please enter a number.")
    else:
        # One way of solving it
        break

print(f"x is {x}")