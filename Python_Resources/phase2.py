# ---------- Defining and Calling Functions ----------
def greet():
    print("Hello!")

greet()

# ---------- Parameters and Return Values ----------
def calculate_total(price, quantity):
    return price * quantity

total = calculate_total(10, 3)
print(f"Total: {total}")

# ---------- Positional and Keyword Arguments ----------
def introduce(name, age):
    print(f"My name is {name} and I am {age} years old.")

introduce("Mona", 25)              # positional
introduce(age=25, name="Mona")     # keyword

# ---------- Default Arguments ----------
def power(base, exponent=2):
    return base ** exponent

print(f"Power with default exponent: {power(5)}")
print(f"Power with custom exponent: {power(5, 3)}")

# ---------- *args and **kwargs ----------
def add_all(*numbers):
    return sum(numbers)

               
def print_details(**info):
    for key, value in info.items():
        print(f"{key}: {value}")
                 
print_details(name="Mona", role="Frontend Developer", city="Lahore")

# ---------- Local vs Global Scope ----------
counter = 0  # global variable

def increment():
    global counter
    counter += 1

increment()
increment()
print(f"Counter after increments: {counter}")

# ---------- Type Hints ----------
def calculate_total_with_hints(price: float, quantity: int) -> float:
    return price * quantity

print(f"Total with type hints: {calculate_total_with_hints(15.5, 2)}")

# ---------- List Comprehension ----------
numbers = [1, 2, 3, 4, 5]
squares = [n ** 2 for n in numbers]
print(f"Squares: {squares}")       

even_numbers = [n for n in numbers if n % 2 == 0]
print(f"Even numbers: {even_numbers}")

# ---------- Dictionary Comprehension ----------
names = ["Ali", "Sara", "Zain"]
name_lengths = {name: len(name) for name in names}
print(f"Name lengths: {name_lengths}")

# ---------- Set Comprehension ----------
unique_lengths = {len(name) for name in names}
print(f"Unique name lengths: {unique_lengths}")

# ---------- Conditional Expressions (ternary) ----------
age = 20
status = "Adult" if age >= 18 else "Minor"
print(f"Status: {status}")