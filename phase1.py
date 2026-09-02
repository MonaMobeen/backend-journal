"""
Phase 1: Python Fundamentals
Covers: variables, types, operators, conditionals, loops, data structures, built-ins
"""

# ---------- Variables & Types ----------
name = "Mona"
age = 25
height = 5.4
is_developer = True

print(f"Name: {name}, Age: {age}, Height: {height}, Developer: {is_developer}")

# ---------- Type Conversion ----------
age_as_text = str(age)
text_number = "100"
number = int(text_number)
print(f"Converted age to text: {age_as_text}, converted text to number: {number}")

# ---------- Operators ----------
a, b = 10, 3
print(f"Sum: {a + b}, Floor Division: {a // b}, Remainder: {a % b}, Power: {a ** 2}")

# ---------- Conditionals ----------
def check_age_group(age):
    if age >= 18:
        return "Adult"
    elif age >= 13:
        return "Teenager"
    else:
        return "Child"

print(f"Age group: {check_age_group(age)}")

# ---------- Loops ----------
print("Even numbers from 0 to 9:")
for i in range(10):
    if i % 2 == 0:
        print(i)

# ---------- break and continue ----------
print("Loop with break and continue:")
for i in range(10):
    if i == 6:
        break
    if i % 2 == 0:
        continue
    print(i)

# ---------- Core Data Structures ----------
# List
fruits = ["apple", "banana", "mango"]
fruits.append("orange")
print(f"Fruits list: {fruits}")

# Tuple
point = (10, 20)
print(f"Point tuple: {point}")

# Set
unique_ids = {1, 2, 2, 3, 3, 3}
print(f"Unique IDs set: {unique_ids}")

# Dictionary
user = {"name": "Mona", "age": 25, "role": "Frontend Developer"}
print(f"User dictionary: {user}")

# ---------- Built-in Functions ----------
nums = [4, 2, 9, 1, 7]
print(f"Length: {len(nums)}")
print(f"Sum: {sum(nums)}")
print(f"Min: {min(nums)}, Max: {max(nums)}")
print(f"Sorted: {sorted(nums)}")

print("Enumerate example:")
for index, value in enumerate(nums):
    print(f"  Index {index}: {value}")

print("Any/All example:")
print(f"Any negative? {any(n < 0 for n in nums)}")
print(f"All positive? {all(n > 0 for n in nums)}")