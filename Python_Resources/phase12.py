from functools import reduce, partial


# ---------- Functions as First-Class Objects ----------
# In Python, functions can be assigned to variables, passed as arguments,
# and returned from other functions - just like any other value (numbers, strings).
def greet(name):
    return f"Hello, {name}!"


say_hello = greet   
print(say_hello("Mona Mobeen"))


# ---------- Pure Functions ----------
# A pure function ALWAYS returns the same output for the same input,
# and has no side effects (doesn't modify anything outside itself).
def add(a, b):  # PURE - depends only on its inputs
    return a + b


total = 0


def add_to_total(value):  # NOT pure - modifies something outside itself
    global total
    total += value
    return total


print(f"Pure function result: {add(2, 3)}")
print(f"Impure function result (changes external state): {add_to_total(5)}")


# ---------- Higher-Order Functions ----------
# A higher-order function either takes a function as an argument,
# or returns a function as its result.
def apply_operation(numbers, operation):
    """Takes a LIST and a FUNCTION, and applies that function to each item."""
    return [operation(n) for n in numbers]


def square(n):
    return n ** 2


def double(n):
    return n * 2


numbers = [1, 2, 3, 4]
print(f"Squared: {apply_operation(numbers, square)}")
print(f"Doubled: {apply_operation(numbers, double)}")


# ---------- map() and filter() ----------
# map() applies a function to every item in a list (similar to apply_operation above)
squared_with_map = list(map(square, numbers))
print(f"Squared with map(): {squared_with_map}")

# filter() keeps only items where the function returns True
def is_even(n):
    return n % 2 == 0


even_numbers = list(filter(is_even, numbers))
print(f"Even numbers with filter(): {even_numbers}")


# ---------- lambda ----------
# lambda creates a small, unnamed (anonymous) function in a single line.
# It's most useful for short, throwaway functions - not for complex logic.
squared_with_lambda = list(map(lambda n: n ** 2, numbers))
print(f"Squared with lambda: {squared_with_lambda}")

even_with_lambda = list(filter(lambda n: n % 2 == 0, numbers))
print(f"Even numbers with lambda: {even_with_lambda}")


# ---------- functools.reduce ----------
# reduce() combines all items in a list into a SINGLE value,
# by repeatedly applying a function to pairs of items.
sum_of_numbers = reduce(lambda acc, n: acc + n, numbers)
print(f"Sum using reduce(): {sum_of_numbers}")

product_of_numbers = reduce(lambda acc, n: acc * n, numbers)
print(f"Product using reduce(): {product_of_numbers}")


# ---------- functools.partial ----------
# partial() creates a new function with some arguments already "pre-filled".
def power(base, exponent):
    return base ** exponent


square_partial = partial(power, exponent=2)  # exponent is now always 2
cube_partial = partial(power, exponent=3)    # exponent is now always 3

print(f"Square using partial(): {square_partial(5)}")
print(f"Cube using partial(): {cube_partial(5)}")


# ---------- Avoiding Clever One-Liners When Readability Suffers ----------
# BAD: hard to read, too much logic crammed into one line
# result = list(filter(lambda x: x % 2 == 0, map(lambda x: x ** 2, [n for n in range(20) if n % 3 == 0])))

# GOOD: broken into clear, named steps - easier to read and debug
def get_multiples_of_three(limit):
    return [n for n in range(limit) if n % 3 == 0]


def square_all(numbers):
    return list(map(lambda n: n ** 2, numbers))


def keep_even_only(numbers):
    return list(filter(lambda n: n % 2 == 0, numbers))


multiples = get_multiples_of_three(20)
squared = square_all(multiples)
final_result = keep_even_only(squared)
print(f"Readable step-by-step result: {final_result}")