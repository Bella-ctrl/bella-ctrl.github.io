def hello(to="world"):
    print("Hello,", to)

hello()
name = input("What is your name? ").strip().title()
hello(name)