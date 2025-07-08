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

    def add_passenger(self, name): # Method to add a passenger
        if not self.open_seat():
            return False
        self.passengers.append(name) # Add the passenger's name to the list
        return True

    def open_seat(self):
        return self.capacity - len(self.passengers)

flight = Flight(3)  # Create a flight with a capacity of 3 passengers
people = ["Alice", "Bob", "Charlie", "David"]
for person in people:
    success = flight.add_passenger(person)
    if success:
        print(f"Added {person} to flight successfully.")
    else:
        print(f"No available seat for {person}.")