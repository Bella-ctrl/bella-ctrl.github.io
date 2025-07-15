def hello(to):
    print("Hello,", to)

name = input("What is your name? ").strip().title()
hello(name)