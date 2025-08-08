def main():
    number = int(input("Enter a number: "))
    print(f"The square of {number} is {square(number)}")

def square(num):
    return num * num

if __name__ == "__main__":
    main()