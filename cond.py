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
if score >= 90 and score <= 100:
    print("A")
elif score >= 80 and score < 90:
    print("B")
elif score >= 70 and score < 80:
    print("C")
elif score >= 60 and score < 70:
    print("D")
else:
    print("F")