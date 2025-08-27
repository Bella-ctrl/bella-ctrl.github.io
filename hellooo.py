## Just to have a commit todat
## Just to have a commit todat
class Hello():
    def __init__(self, name, last):
        self.name = name
        self.last = last

    def __str__(self):
        return f"Hello {self.name} {self.last}, nice to meet you!"

def main():
    name = input("Introduce your name: ")
    last = input("Introduce your last name: ")
    print(Hello(name, last))

if __name__ == "__main__":
    main()