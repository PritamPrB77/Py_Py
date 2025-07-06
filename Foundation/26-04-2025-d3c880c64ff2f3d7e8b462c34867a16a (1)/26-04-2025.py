# to run this file : python 26-04-2025.py
try :
    val_1 = int(input("Value 1 : Enter a number : "))
except :
    print("Error : Value is not a number")
    print("Handling by using 0 as number")
    val_1 = 0

try :
    val_2 = int(input("Value 2 : Enter a number : "))
except :
    print("Error : Value is not a number")
    print("Handling by using 0 as number")
    val_2 = 0

try :
    val_3 = int(input("Value 3 : Enter a number : "))
except :
    print("Error : Value is not a number")
    print("Handling by using 0 as number")

    val_3 = 0

# ctrl + ~ --> windows
# command + ~
# command + j --> mac

def add(val_1, val_2):
    c = val_1 + val_2
    print("Result of addition is : ", c)
    return c

print("Running add function with values : ", val_1, " ", val_2)
answer = add(val_1, val_2)
print("Add function executed successfully")

print("Running add function with values : ", answer, " ", val_3)
add(answer, val_3)
print("Add function executed successfully")

