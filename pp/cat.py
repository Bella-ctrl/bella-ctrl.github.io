# for i in range(3):
    # For i in [0, 1, 2]
    # print("Meow")

#while True:
#    n = int(input("Enter a number (0 to exit): "))
 ##      break

#for i in range(n):
 #   print("Meow")

def main():
    number = get_number()
    meow(number)

def get_number():
    while True:
        n = int(input("Enter a number (0 to exit): "))
        if n > 0:
            break
    return n

def meow(n):
    for _ in range(n):
        print("Meow")

main()