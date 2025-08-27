## Just to have a commit todat
## Just to have a commit todat
class Hello():
    def __init__(self, name):
        self.name = name

    def __str__(name):
        return f"Hello {self.name}, nice to meet you!"

def main():
    salute = Hello()
    name = input("Introduce your name: ")
    print(Hello(name))

if __name__ == "__main__":
    main()