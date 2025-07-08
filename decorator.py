# Decorators allow to modify a function's behavior by taking a function as an argument and returning a new function.

def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Function has finished running.")
    return wrapper

@announce # to use the decorator
def hello():
    print("Hello, World")
