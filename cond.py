# Conditionals: forks on roads
### symbols:
#### > >= < <= == !=

#x = int(input("What's X? "))
#y = int(input("What's Y? "))

#if x < y:
 #   print("X is less than Y")
#elif x > y:
  #  print("X is greater than Y")
#else:
 #   print("X is equal to Y")

###if x < y or x > y:
   # print("X is not equal to Y")
#else:
   # print("X is equal to Y")


score = int(input("Score: "))
if 90 <= score <= 100:
    # score >= 90
    print("A")
elif 80 <= score < 90:
    # score >= 80
    print("B")
elif 70 <= score < 80:
    # score >= 70           
    print("C")
elif 60 <= score < 70:
    # score >= 60
    print("D")
else:
    print("F")