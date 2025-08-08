from a import square

def main():
    test_square()

# Convention to call test functions with 'test_' prefix
def test_square():
    ### Try - AssertionError 
        assert square(2) == 4
        assert square(3) == 9
        

    # Alternatively, without assert statements:
    ##if square(2) != 4:
     ###   print("2 squared was not 4")
    ##if square(3) != 9:
     ###   print("3 squared was not 9")
    
if __name__ == "__main__":
    main()