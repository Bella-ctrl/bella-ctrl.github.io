# Dictionary of students
#students = {
 #   "Hermione": "Gryffindor",
  # "Ron": "Gryffindor",
   # "Draco": "Slytherin",
#}

#for student in students:
 #   print(f"{student} is in {students[student]}")


students = [
    {"name": "Hermione", "house": "Gryffindor", "patronus": "Otter"},
    {"name": "Harry", "house": "Gryffindor", "patronus": "Stag"},
    {"name": "Ron", "house": "Gryffindor", "patronus": "Jack Russell Terrier"},
    {"name": "Draco", "house": "Slytherin", "patronus": "None"},
]

for student in students:
    print(f"Name: {student['name']}, House: {student['house']}, Patronus: {student['patronus']}")

def print_column(height):
    print("#\n" * height, end="")

def print_row(width):
    print("?" * width)

def main():
    print_column(5)
    print_row(5)
    print_square(5)

def print_square(size):
    # Print a square of bricks
    for i in range(size):
        #for each brick in the row
        for j in range(size):
            # print brick
            print("#", end="")
        print()
main()

# List of students
#students = ["Hermione", "Harry", "Ron"]

#for i in range(len(students)):
#for student in students:
 #   print(i + 1, students[i])
    #print(students[i])


#print(students[0])



