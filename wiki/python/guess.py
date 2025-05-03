import random

# Introduction to mini game
name = input("Tell us the name of the one that'll lose today: ")
print(f"Hello, {name}, are you ready to be a sore loser?")
print("If you are, then get ready to start guessing a number while little computer thinks of a number")

randomNumber = random.randint(0, 20)
print("Done, little C has already thought of a number.")
print("Give us your best guess of a what number he thought of between 0 and 20, you have three chances.")

tries = 0
for i in range(3):
    tries += 1
    guess = int(input("Your guess is: "))
    if guess == randomNumber: 
        print("You've guessed correctly. Congrats")
        exit(1)
    else:
        print(f"You've guessed incorrectly. This is your {tries} of 3. You have {3 - tries} left.")
        if tries == 3:
            print(f"The correct number was {randomNumber}")
