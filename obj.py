# Object Oriented Programming (OOP) in Python

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(2, 8)
print(p.x)  # Output: 2
print(p.y)  # Output: 8


class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = [] # List to store passengers that starts empty

flight = Flight(3)  # Create a flight with a capacity of 3 passengers