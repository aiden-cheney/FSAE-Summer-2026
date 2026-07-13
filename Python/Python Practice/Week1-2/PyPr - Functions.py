# ============================================================
# BEGINNER PYTHON NOTES + PRINTED RESULT GUIDE
# ============================================================
# This file explains beginner Python topics.
# Each section has comments explaining the code.
# Print statements label each result clearly.
# Run this file from top to bottom.
# ============================================================


# ============================================================
# 1. VARIABLES
# ============================================================

# Variables store information for later.
# Use clear names for readability.
# Strings store text inside quotes.
# Integers store whole numbers.
# Python uses = to assign values.
# The left side is the variable name.
# The right side is the stored value.

print("\n==================== 1. VARIABLES ====================")

name = "Aiden"   # Stores text in variable name.
age = 18         # Stores whole number in age.

print("The variable 'name' stores:", name)
print("The variable 'age' stores:", age)


# ============================================================
# 2. VALID AND INVALID VARIABLE NAMES
# ============================================================

# Variable names cannot start with numbers.
# Variable names cannot use symbols like !.
# Variable names cannot be Python keywords.
# Good names explain what they store.
# Use underscores for multiple words.
# Example: student_age is readable.

print("\n==================== 2. VARIABLE NAMING RULES ====================")

student_age = 18       # Valid variable name.
favorite_color = "red" # Valid variable name.

print("student_age is a valid variable name:", student_age)
print("favorite_color is a valid variable name:", favorite_color)

# Invalid examples:
# 123name = "Aiden"  # Cannot start with number.
# !age = 18          # Cannot use symbol.
# for = "hi"         # Cannot use Python keyword.


# ============================================================
# 3. EXPRESSIONS VS STATEMENTS
# ============================================================

# Expression returns a value.
# Statement performs an action.
# 1 + 1 is an expression.
# print() is a statement.
# Expressions can go inside print().
# Statements usually do something visible.

print("\n==================== 3. EXPRESSIONS VS STATEMENTS ====================")

print("Expression 1 + 1 returns:", 1 + 1)
print("Expression 'Aiden' returns:", "Aiden")
print("Statement print(name) displays:", name)


# ============================================================
# 4. COMMENTS
# ============================================================

# Comments are ignored by Python.
# Comments explain what code does.
# Comments start with a hashtag.
# Comments help you understand later.
# Comments do not affect output.

print("\n==================== 4. COMMENTS ====================")

print("Comments are ignored unless you explain them with print().")


# ============================================================
# 5. STRINGS
# ============================================================

# Strings store text.
# Strings use quotation marks.
# Single or double quotes work.
# Strings can contain letters.
# Strings can contain numbers too.
# Numbers in strings are not math numbers.

print("\n==================== 5. STRINGS ====================")

name = "Aiden"       # Text stored as string.
number_text = "80"   # Number stored as text.

print("name is a string:", name)
print("number_text is also a string:", number_text)
print("The type of name is:", type(name))
print("The type of number_text is:", type(number_text))


# ============================================================
# 6. INTEGERS AND FLOATS
# ============================================================

# Integers are whole numbers.
# Floats are decimal numbers.
# int means integer.
# float means decimal number.
# 18 is an integer.
# 18.0 is a float.

print("\n==================== 6. INTEGERS AND FLOATS ====================")

age = 18        # Whole number integer.
height = 5.9    # Decimal number float.

print("age stores an integer:", age)
print("height stores a float:", height)
print("The type of age is:", type(age))
print("The type of height is:", type(height))


# ============================================================
# 7. TYPE CHECKING
# ============================================================

# type() tells the data type.
# isinstance() checks a data type.
# It returns True or False.
# True means the check passed.
# False means the check failed.

print("\n==================== 7. TYPE CHECKING ====================")

name = "Aiden"
age = 18

print("Checking if name is a string using type():", type(name) == str)
print("Checking if name is a string using isinstance():", isinstance(name, str))
print("Checking if age is an integer:", isinstance(age, int))
print("Checking if age is a float:", isinstance(age, float))


# ============================================================
# 8. TYPE CONVERSION
# ============================================================

# Type conversion changes data type.
# int() converts to integer.
# float() converts to decimal.
# str() converts to string.
# Useful when working with input.
# input() always gives strings.

print("\n==================== 8. TYPE CONVERSION ====================")

number = "80"              # This is text.
number_as_int = int(number) # Converts text to integer.
my_age = float(18)          # Converts integer to float.
text_age = str(18)          # Converts integer to string.

print("Original number as string:", number)
print("Converted number using int():", number_as_int)
print("Converted age using float():", my_age)
print("Converted age using str():", text_age)

print("Type of number:", type(number))
print("Type of number_as_int:", type(number_as_int))
print("Type of my_age:", type(my_age))
print("Type of text_age:", type(text_age))


# ============================================================
# 9. OTHER DATA TYPES
# ============================================================

# bool stores True or False.
# list stores many values.
# tuple stores unchangeable values.
# range stores number sequences.
# dict stores key-value pairs.
# set stores unique unordered values.

print("\n==================== 9. OTHER DATA TYPES ====================")

is_student = True                 # Boolean value.
colors = ["red", "blue"]          # List value.
coordinates = (3, 4)              # Tuple value.
numbers_range = range(5)          # Range value.
person = {"name": "Aiden"}        # Dictionary value.
unique_numbers = {1, 2, 2, 3}     # Set removes duplicates.

print("Boolean example:", is_student)
print("List example:", colors)
print("Tuple example:", coordinates)
print("Range example as list:", list(numbers_range))
print("Dictionary example:", person)
print("Set example removes duplicates:", unique_numbers)


# ============================================================
# 10. ARITHMETIC OPERATORS
# ============================================================

# + adds numbers.
# - subtracts numbers.
# * multiplies numbers.
# / divides numbers.
# % gives the remainder.
# ** raises to a power.
# // does floor division.
# Floor division rounds down.

print("\n==================== 10. ARITHMETIC OPERATORS ====================")

print("1 + 1 means addition. Result:", 1 + 1)
print("2 - 1 means subtraction. Result:", 2 - 1)
print("2 * 2 means multiplication. Result:", 2 * 2)
print("4 / 2 means regular division. Result:", 4 / 2)
print("4 % 3 gives the remainder. Result:", 4 % 3)
print("4 ** 2 means 4 squared. Result:", 4 ** 2)
print("5 // 2 means floor division. Result:", 5 // 2)


# ============================================================
# 11. STRING CONCATENATION
# ============================================================

# Concatenation combines strings.
# Use + between strings.
# Both values must be strings.
# Add spaces manually when needed.
# "Aiden" + "Hi" has no space.
# "Aiden" + " Hi" has space.

print("\n==================== 11. STRING CONCATENATION ====================")

first_name = "Aiden"
sentence = first_name + " is the best"

print("first_name stores:", first_name)
print("Concatenated sentence is:", sentence)


# ============================================================
# 12. ASSIGNMENT OPERATORS
# ============================================================

# += adds and updates variable.
# -= subtracts and updates variable.
# *= multiplies and updates variable.
# /= divides and updates variable.
# age += 8 means age = age + 8.
# These save space in code.

print("\n==================== 12. ASSIGNMENT OPERATORS ====================")

age = 8
print("Starting value of age:", age)

age += 8
print("After age += 8, age is:", age)

score = 20
print("Starting value of score:", score)

score -= 5
print("After score -= 5, score is:", score)

aiden = 19
print("Starting value of aiden:", aiden)

aiden *= 8
print("After aiden *= 8, aiden is:", aiden)


# ============================================================
# 13. COMPARISON OPERATORS
# ============================================================

# == checks if equal.
# != checks if not equal.
# > checks greater than.
# < checks less than.
# >= checks greater or equal.
# <= checks less or equal.
# Comparisons return True or False.

print("\n==================== 13. COMPARISON OPERATORS ====================")

a = 1
b = 2

print("a stores:", a)
print("b stores:", b)

print("a == b checks equality. Result:", a == b)
print("a != b checks not equal. Result:", a != b)
print("a > b checks greater than. Result:", a > b)
print("a < b checks less than. Result:", a < b)
print("a >= b checks greater/equal. Result:", a >= b)
print("a <= b checks less/equal. Result:", a <= b)


# ============================================================
# 14. BOOLEAN VALUES
# ============================================================

# Booleans are True or False.
# True must be capitalized.
# False must be capitalized.
# Booleans help with decisions.
# if statements use booleans.
# Comparisons create booleans.

print("\n==================== 14. BOOLEAN VALUES ====================")

condition_one = True
condition_two = False

print("condition_one stores:", condition_one)
print("condition_two stores:", condition_two)


# ============================================================
# 15. BOOLEAN OPERATORS
# ============================================================

# not flips True/False.
# and requires both True.
# or requires at least one True.
# Boolean logic controls decisions.
# These return True or False.
# Sometimes they return actual values.

print("\n==================== 15. BOOLEAN OPERATORS ====================")

condition_one = True
condition_two = False

print("not condition_one gives:", not condition_one)
print("condition_one and condition_two gives:", condition_one and condition_two)
print("condition_one or condition_two gives:", condition_one or condition_two)


# ============================================================
# 16. OR WITH NON-BOOLEAN VALUES
# ============================================================

# or returns first truthy value.
# 0 counts as falsey.
# False counts as falsey.
# Non-empty strings are truthy.
# Nonzero numbers are truthy.
# Useful for fallback values.

print("\n==================== 16. OR WITH NON-BOOLEAN VALUES ====================")

print("0 or 1 returns first truthy value:", 0 or 1)
print("False or 'hey' returns first truthy value:", False or "hey")
print("1 or 2 returns 1 because 1 is truthy:", 1 or 2)


# ============================================================
# 17. AND WITH NON-BOOLEAN VALUES
# ============================================================

# and checks first value first.
# If first is falsey, returns first.
# If first is truthy, returns second.
# Empty values usually count false.
# Filled values usually count true.
# This can look confusing initially.

print("\n==================== 17. AND WITH NON-BOOLEAN VALUES ====================")

print("0 and 1 returns 0 because 0 is falsey:", 0 and 1)
print("1 and 0 returns second value 0:", 1 and 0)
print("'hi' and 'hey' returns second value:", "hi" and "hey")
print("False and 0 returns False immediately:", False and 0)


# ============================================================
# 18. STRING METHODS
# ============================================================

# Methods are actions on values.
# .upper() makes uppercase.
# .lower() makes lowercase.
# .islower() checks lowercase.
# Methods use dot notation.
# Dot notation means value.method().

print("\n==================== 18. STRING METHODS ====================")

print("'Aiden'.upper() makes uppercase:", "Aiden".upper())
print("'Aiden'.lower() makes lowercase:", "Aiden".lower())
print("'Person'.islower() checks lowercase:", "Person".islower())
print("'person'.islower() checks lowercase:", "person".islower())


# ============================================================
# 19. ESCAPE CHARACTERS
# ============================================================

# Backslash escapes special characters.
# \" adds quotes inside string.
# \n creates a new line.
# Useful for formatting text.
# Escape characters start with backslash.
# They change how strings display.

print("\n==================== 19. ESCAPE CHARACTERS ====================")

jeep = "\"Aiden\""

print("Using \\\" puts quotes inside text:", jeep)
print("Using \\n creates a new line:")
print("Line one\nLine two")


# ============================================================
# 20. MULTI-LINE STRINGS
# ============================================================

# Triple quotes make multi-line strings.
# They preserve line breaks.
# Useful for long text.
# Can use three double quotes.
# Can also use three single quotes.
# Print displays all lines.

print("\n==================== 20. MULTI-LINE STRINGS ====================")

multi_line = """Aiden is my name.

You are the best."""

print("This multi-line string prints across lines:")
print(multi_line)


# ============================================================
# 21. STRING INDEXING
# ============================================================

# Indexing gets one character.
# Indexes start at zero.
# First character is index 0.
# Negative indexes count backward.
# -1 means last character.
# Use square brackets for indexes.

print("\n==================== 21. STRING INDEXING ====================")

name = "aiden"

print("The string name is:", name)
print("name[0] gets first character:", name[0])
print("name[1] gets second character:", name[1])
print("name[-1] gets last character:", name[-1])


# ============================================================
# 22. STRING SLICING
# ============================================================

# Slicing gets part of string.
# Format is string[start:end].
# Start index is included.
# End index is not included.
# name[0:3] gets indexes 0,1,2.
# Slicing can return empty string.

print("\n==================== 22. STRING SLICING ====================")

name = "aiden"

print("name[0:3] gets index 0 through 2:", name[0:3])
print("name[1:4] gets index 1 through 3:", name[1:4])
print("name[:3] starts at beginning:", name[:3])
print("name[2:] goes to the end:", name[2:])
print("name[-1:3] gives empty result:", name[-1:3])


# ============================================================
# 23. TRUTHY AND FALSEY VALUES
# ============================================================

# Empty strings are falsey.
# Non-empty strings are truthy.
# 0 is falsey.
# Nonzero numbers are truthy.
# Empty lists are falsey.
# These matter in if statements.

print("\n==================== 23. TRUTHY AND FALSEY VALUES ====================")

done = ""

print("done stores an empty string:", done)
print("type(done) == bool checks if done is bool:", type(done) == bool)

if done:
    print("done is truthy, so this prints yes")
else:
    print("done is falsey, so this prints no")


# ============================================================
# 24. ANY FUNCTION
# ============================================================

# any() checks multiple values.
# It returns True if one is True.
# It returns False if none are True.
# Put values inside a list.
# Useful for checking several conditions.
# One true value is enough.

print("\n==================== 24. ANY FUNCTION ====================")

book1 = True
book2 = False

read_any_book = any([book1, book2])

print("book1 stores:", book1)
print("book2 stores:", book2)
print("any([book1, book2]) result:", read_any_book)


# ============================================================
# 25. ALL FUNCTION
# ============================================================

# all() checks multiple values.
# It returns True if all are True.
# It returns False if one is False.
# Put values inside a list.
# Useful when everything must pass.
# One false value makes False.

print("\n==================== 25. ALL FUNCTION ====================")

book1 = True
book2 = False

read_all_books = all([book1, book2])

print("book1 stores:", book1)
print("book2 stores:", book2)
print("all([book1, book2]) result:", read_all_books)


# ============================================================
# 26. COMPLEX NUMBERS
# ============================================================

# Complex numbers have real part.
# Complex numbers have imaginary part.
# j means imaginary number.
# .real gets real part.
# .imag gets imaginary part.
# complex(a,b) creates a+bj.

print("\n==================== 26. COMPLEX NUMBERS ====================")

num1 = 2 + 3j
num2 = complex(2, 3)

print("num1 stores complex number:", num1)
print("num2 stores complex number:", num2)
print("num2.real gets real part:", num2.real)
print("num2.imag gets imaginary part:", num2.imag)


# ============================================================
# 27. NUMBER FUNCTIONS
# ============================================================

# abs() gives absolute value.
# round() rounds numbers.
# round(number, digits) controls decimals.
# Useful for cleaner output.
# Functions take values in parentheses.
# Functions return a result.

print("\n==================== 27. NUMBER FUNCTIONS ====================")

print("abs(-10) gives positive distance from zero:", abs(-10))
print("round(5.4763830, 4) rounds to 4 decimals:", round(5.4763830, 4))
print("round(5.6) rounds to nearest integer:", round(5.6))


# ============================================================
# 28. ENUMS
# ============================================================

# Enums create named constants.
# Import Enum before using.
# Class defines enum group.
# Names should be uppercase.
# Values usually stay constant.
# Enums improve code readability.

print("\n==================== 28. ENUMS ====================")

from enum import Enum

class State(Enum):
    INACTIVE = 0
    ACTIVE = 1

print("State.ACTIVE gives enum member:", State.ACTIVE)
print("State.ACTIVE.value gives stored value:", State.ACTIVE.value)
print("State(1) finds member by value:", State(1))
print("State['ACTIVE'] finds member by name:", State["ACTIVE"])
print("State['ACTIVE'].value gives value:", State["ACTIVE"].value)
print("list(State) lists all enum members:", list(State))
print("len(State) counts enum members:", len(State))


# ============================================================
# 29. USER INPUT
# ============================================================

# input() asks user for text.
# input() always returns string.
# Convert input for math.
# int(input()) makes integer input.
# This section is commented out.
# Uncomment when practicing input.

print("\n==================== 29. USER INPUT ====================")

# user_age = input("Enter your age: ")
# print("input() returned this string:", user_age)
# print("The type of user_age is:", type(user_age))

print("Input code is commented out so the program does not pause.")


# ============================================================
# 30. IF STATEMENTS
# ============================================================

# if checks a condition.
# else runs if condition fails.
# Indentation matters in Python.
# Code inside if is indented.
# Conditions usually return booleans.
# if condition: is cleaner than == True.

print("\n==================== 30. IF STATEMENTS ====================")

condition = True

print("condition stores:", condition)

if condition == True:
    print("Because condition == True, this prints Aiden.")
else:
    print("Because condition == True is false, this prints Hello.")

if condition:
    print("Cleaner version also prints Aiden.")
else:
    print("Cleaner version would print Hello.")


# ============================================================
# 31. LISTS
# ============================================================

# Lists store multiple values.
# Lists use square brackets.
# Lists can hold mixed types.
# Each item has an index.
# Indexes start at zero.
# Lists can be changed.

print("\n==================== 31. LISTS ====================")

aiden = 19

dogs = [aiden, 5, 7, "Ethan", True]

print("The full dogs list is:", dogs)
print("dogs[0] gets first item:", dogs[0])
print("dogs[4] gets fifth item:", dogs[4])


# ============================================================
# 32. CHECKING ITEMS IN LISTS
# ============================================================

# in checks list membership.
# It returns True or False.
# Must match exact value.
# Strings are case-sensitive.
# "Aiden" differs from "aiden".
# Useful for searching lists.

print("\n==================== 32. CHECKING ITEMS IN LISTS ====================")

dogs = [19, 5, 7, "Ethan", True]

print("'Ethan' in dogs checks membership:", "Ethan" in dogs)
print("'Aiden' in dogs checks membership:", "Aiden" in dogs)
print("19 in dogs checks membership:", 19 in dogs)


# ============================================================
# 33. CHANGING LIST ITEMS
# ============================================================

# Lists are mutable.
# Mutable means changeable.
# Use index to replace item.
# list[0] changes first item.
# Assignment updates the list.
# Original value gets replaced.

print("\n==================== 33. CHANGING LIST ITEMS ====================")

dogs = [19, 5, 7, "Ethan", True]

print("Before changing, dogs is:", dogs)

dogs[0] = "Blue"

print("After dogs[0] = 'Blue', dogs is:", dogs)
print("dogs[0] is now:", dogs[0])


# ============================================================
# 34. LIST SLICING
# ============================================================

# List slicing gets multiple items.
# Format is list[start:end].
# Start index is included.
# End index is not included.
# Works like string slicing.
# Returns a smaller list.

print("\n==================== 34. LIST SLICING ====================")

dogs = ["Blue", 5, 7, "Ethan", True]

print("The dogs list is:", dogs)
print("dogs[1:3] gets indexes 1 and 2:", dogs[1:3])
print("dogs[:2] gets first two items:", dogs[:2])
print("dogs[2:] gets index 2 onward:", dogs[2:])


# ============================================================
# 35. LIST LENGTH
# ============================================================

# len() counts list items.
# It returns an integer.
# Works on strings too.
# Useful for loops later.
# Empty list length is zero.
# Length is not last index.

print("\n==================== 35. LIST LENGTH ====================")

dogs = ["Blue", 5, 7, "Ethan", True]

print("The dogs list is:", dogs)
print("len(dogs) counts list items:", len(dogs))
print("Last index is length minus one:", len(dogs) - 1)


# ============================================================
# 36. APPENDING TO LISTS
# ============================================================

# append() adds one item.
# It adds to the end.
# Spelling is append, not appened.
# append changes original list.
# Use dot notation.
# Format: list.append(value)

print("\n==================== 36. APPENDING TO LISTS ====================")

dogs = ["Blue", 5, 7, "Ethan", True]

print("Before append, dogs is:", dogs)

dogs.append("Jenny")

print("After dogs.append('Jenny'), dogs is:", dogs)


# ============================================================
# 37. REMOVING FROM LISTS
# ============================================================

# remove() removes a value.
# It removes first matching value.
# Value must exist in list.
# Otherwise Python gives error.
# remove changes original list.
# Format: list.remove(value)

print("\n==================== 37. REMOVING FROM LISTS ====================")

dogs = ["Blue", 5, 7, "Ethan", True, "Jenny"]

print("Before remove, dogs is:", dogs)

dogs.remove("Jenny")

print("After dogs.remove('Jenny'), dogs is:", dogs)


# ============================================================
# 38. INSERTING ONE ITEM
# ============================================================

# insert() adds item at index.
# Existing items shift right.
# Format: list.insert(index, value).
# Index tells where to place.
# insert changes original list.
# Useful for specific placement.

print("\n==================== 38. INSERTING ONE ITEM ====================")

items = ["Aiden", "Jen", "Dave", "Ian"]

print("Original items list:", items)

items.insert(2, "Him")

print("After items.insert(2, 'Him'), items is:", items)


# ============================================================
# 39. INSERTING MULTIPLE ITEMS
# ============================================================

# Slice assignment inserts multiple items.
# list[2:2] inserts at index 2.
# Nothing is removed here.
# New items shift others right.
# Useful for adding many values.
# This is different from insert().

print("\n==================== 39. INSERTING MULTIPLE ITEMS ====================")

items = ["Aiden", "Jen", "Dave", "Ian"]

print("Original items list:", items)

items[2:2] = ["balls", "butt"]

print("After items[2:2] = ['balls', 'butt'], items is:", items)


# ============================================================
# 40. SORTING LISTS
# ============================================================

# sort() orders the list.
# Strings sort alphabetically.
# Numbers sort numerically.
# sort changes original list.
# All items should match type.
# Mixed types can cause errors.

print("\n==================== 40. SORTING LISTS ====================")

items = ["Aiden", "Jen", "Dave", "Ian"]

print("Before sorting strings:", items)

items.sort()

print("After items.sort():", items)

numbers = [5, 2, 9, 1, 3]

print("Before sorting numbers:", numbers)

numbers.sort()

print("After numbers.sort():", numbers)

#tupples allows teh userto mak eimmuteble gourp of objects means you cannot add or romve items using petheis nstad of sqaure brckts 
blue = ("roger", "syd")

blue[0]

blue.index("roger")
len(blue)
print("roger" in blue)

#docitonaries aloow you to create key value paies (key firts thins cna be any umutable value lat thign can be anythign )
dog = {"name" : "Roger", "age": 8}

print (dog ["name"])

print (list(dog.keys()))
print (list(dog.values()))
print (list(dog.items()))

del dog ['age']

#sets worl lek touples but not ordered and mutable liek a distionary byt ot key value paries 

set1 = {"aiden", "Tegan"}
set2 = {"aiden", "Luna"}

intersect = set1 & set2
print(intersect)

mod = set2 | set1
print (mod)

mode = set2 - set1
print (mode)

modee = set2 > set1
print (modee)
