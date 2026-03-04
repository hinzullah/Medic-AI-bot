'''print("Hello, World!")
# This is a simple Python script that prints "Hello, World!" to the console.
name = "Alice"
age = 24
height = 5.5
is_student = True
print("My name is " + name + ", I am " + str(age) + " years old, My height is " + str(height) + " feet and my student status is " + str(is_student))

num_string = "15"
num_integer = int(num_string)
print("The integer value is : " + str(num_integer))'''

'''name = input("Enter your name: ")
age = input("Enter your real age: ")
height = input("Enter your height in feet: ")
is_student = input("Are you a student? (yes/no): ")
print("My name is " + name + ", I am " + age + " years old, My height is " + height + " feet and my student status is " + is_student + ".")'''

age = 10
if age < 18:
    print("you are not eligible to vote.")
elif age >= 18:
    print("You are eligible to vote henceforth.")
else:
    print("Invalid age.")

status = 404
match status:
    case 200:
        print("OK")
    case 500:
        print("Internal Server Error")
    case 404:
        print("Not Found!")
    case _:
        print("Unknown Status")