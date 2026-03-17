"""
This is a mulit-line comment / string
Welcome to python 101

"""

# this is a single line commment

"""
 - single comments & multi-line comment/ string
 - variable (hold references to what has been stored in memory. It can only be used after defined)
"""
name = "John Doe" # this is a variable
name = "Peter Jane" # this is called variable overriding
output ="" # global variable
age = 12
weight = 12.4

# variable overriding => we reassign the value of the variable
output = age
output = weight


# DATA-TYPES: TEXT | NUMBERS | LISTS 
"""
DATA TYPES: 
    - Text: str() -> list of characters enclosed inside quotation marks(either '' or ""). 
    - Numbers: int(), complex(), float() 
    - Lists: array, set, tuple, dictionary

"""

""" 
NUMBERS: 
    - integer: values that span from 0 ->  infinity and 0 -> -ve infinity, DO NOT HAVE decimals. 
    integers have a class int()

    - float: values that have decimals. Have a class of float()

    - complex: sqaure-root of -2 => complex number. Have a class of complex().
    in complex numbers we use the keyword j after the number

"""
numberOne = 10 # integer
output = numberOne # returns the value of number One
output = type(numberOne) # returns the data type

weightOne = 20.5 # floating 
output = weightOne # returns the value of weightOne
output = type(weightOne) # returns the data type

complexNumberOne = 2j # complex
output = complexNumberOne # returns the value of complexNumberOne
output = type(complexNumberOne) # returns the data type

numberOne = 12
output = float(numberOne) # it parsing the value to a floating point number
output = int(numberOne) # it has parsed the value back to integer
output = complex(numberOne) # it is being parsed to a complex number

"""
Operators & Operands:
    e.g. x + y = 10 .... find x : x and y are called operands and + and = are called operators
    - operators: 
        +(add)
        -(minus) 
        /(division)
        *(multiplication)
        //(floor division)
        **(power) 
        %(modulus)
"""

numberOne = 10
numberTwo = 20
# numberTwo = 3 # overrided the value of numberTwo

output  = numberOne + numberTwo # addition 
output  = numberOne - numberTwo # subraction
output  = numberOne / numberTwo # division
output  = numberOne // numberTwo # floor division => truncates
output  = numberOne * numberTwo # mulitiplication
output  = numberOne ** numberTwo # power 
numberTwo = 3
numberTwo = 7
output  = numberOne % numberTwo # modulus => returns the remainder


# userMathProblem = input("Hey, kindly input the problem you would like us to solve: ")
# output = eval(userMathProblem) # execute python scripts but has no control over which python scripts not to execute -> opens doors to possible malicious attacks


"""
COMPARISON OPERATORS: 
     - Answer the question: How does a compare with b? are they equal? 
      Is one smaller or bigger? or are they less than or equal to or greater than or equal to?
      - greater than (>)
      - less than(<)
      - greater than or equal to (>=)
      - less than or equal to (<=)
      - equality (==)
"""
numberThree = 20 
numberFour = 40 
output = numberThree == numberFour # check for equality between numberThree and numberFour
output = numberThree > numberFour # check for whether numberThree is greater than numberFour
output = numberThree < numberFour # check for whether numberThree is less than numberFour
output = numberThree <= numberFour # check for whether numberThree is less than or equal to numberFour
output = numberThree >= numberFour # check for whether numberThree is greater than or equal to numberFour

# BOOLEAN OPERATORS: and, or, not (TRUTH TABLE)
isRaining = True
areLightsOn = False

age = 18
height = 150

output = (age < 20 and height > 200)
output = (age < 20 or height > 200)
output = not(age < 20 or height > 200)
output = not(age < 20 and height > 200)

#  Assignment operators: +=, -=, /=, *=, //=, =

numberOne = 10
numberTwo = 11

output = numberOne + numberTwo
numberOne += numberTwo
output = numberOne
# numberOne += numberTwo
# numberOne *= numberTwo
# numberOne /= numberTwo
# numberOne //= numberTwo
# numberOne **= numberTwo
i = 0
# i = i+1
# i+=1

# identity(is ... is not ) & membership(in) operators
# fruits = ['mangoe','banana','apple', 'watermelons']

# output = 'apple' in fruits

# STRINGS: str() => placed inbetween '' or ""
name = "John Doe"
name = "Tonny's"

# mulitiline string
bio = """
My name is JOhn Doe, I am a data scientist based in Kenya focusing
 on Health-care analytics.
My core tools of trade are  Python,  Streamlit, Pandas and Colan
"""

output = name
output = bio

output = name[5] # accessing string characters using the index (counting in computers start from 0 ... n-1)
output = name[-1]
output = name[0:6] # slicing 
output = name[2:8]
output= name[-1:]
output= name[4:]
name = "John Doe" # instance of the string class 
output = name[0:8:2] # slicing with a step or 2 => Jh oe

# strings methods
output = name.upper()
output = name.lower()
output = name.replace('o','u')


ten ="10"
output = int(ten) 
output = type(int(ten))

name = "John Wick Doe"
output = len(name)
output=  name[12]
name = "John Doe" # instance of the string class 
output = name[0:8:1] # slicing with a step or 2 => Jh oe



output = "Hello WORLD!! "
output = id(output) # represents memory locatoin


"""
CONTROL FLOWS: 
    - if...else
    - ternary operatot
    - match
    - if ... elif ... else

note: code is grouped using indentation

"""

# if...else

age = 10
year = 2026

if age>18:
    output = "Go vote"

if (age > 18): 
    output = "Go Vote!"
else: 
    output = "Smile!"

# ternary operator
output  = "Go vote" if age >18 else "smile"

if age > 18:
    output = "Go vote!" 
else:
    output = "you can go home and have ice cream"


if (age <= 10)  or (year == 2025): 
    output = "Go and learn graphic design"
else: 
    output = "Go read!"


shoeColor = "green"
pantsColor = "black"

# if ... elif ... else
if (shoeColor == "black") and (pantsColor == "yellow"):
    output = "We are not looking for balck yellow color!"

elif (shoeColor == "yellow") and (pantsColor == "purple"):
    output = "Oii! this is not right!!"

elif (shoeColor == "blue") and (pantsColor == "white"):
    output = "This is nice but not today!"

else: 
    output =" Oi!! you can go back home!"

color = "magenta"

# match case
match(color):
    case "blue":
        output = "Blue looks good!"
    case "yellow":
        output = "Yellow is bright that is fun"
    case "green":
        output = "Green is for prosperity we need that!"
    case _:
        output = "Colors are quite confusing!"


# iterations (for loop, while loop, range())
name = "Spider Woman" # strings are IMMUTABLE lists

#  for loop
for l in name:
    # if l.lower() == "s":
    #     break # stops the loop
    if l == "p":
        continue # skip that scenario
    # print(l)

for num in range(3, 11):
    # print(num)
    if num == 4:
        continue # skipped 
    if num == 8:
        break # stopped

# while loops

start = 10
stop = 20

while (start < stop):
    # print(start)
    start +=1

# Python Data structure (List, Tuple, set,Dict) 

# lists => mutable collection of items or rather elments(you can have more htan one data type in a list)
fruits = ["apples", "bananas", "mangos","pineapples","kiwi"]
grandmasGarden = ["potatoes", "cabbages", "mangoes", "tomatoes"]

output = fruits
output = fruits[2]
output = fruits[1:4] # slicing 
fruits.append("watermelon")
fruits.pop()
fruits.insert(0,"tomatoe")
fruits.insert(len(fruits),"passion")
fruits.insert(len(fruits),"avocado")
fruits.remove("avocado")
fruits.pop(3)
fruits.insert(len(fruits),"passion")
fruits.insert(len(fruits),"passion")
fruits.insert(len(fruits),"passion")

fruits = fruits + grandmasGarden # concetation of lists

output = fruits.count("passion")

fruits[0] = "onions"
output = fruits

# for fruit in fruits:
#     print(fruit)


#  tuples : immutable

colors = ("blue","green", "yellow")

output = colors
output = type(colors)
# colors[0] = "red" # tuple is immutable 
output = colors

# dictionary
person = {
    "name": "Maria Martha",
    "age":12,
    "hobbies":["drawing","music", "dancing","reading"],
}

output = person["age"]



print("===============================")
print(output)
print("===============================")