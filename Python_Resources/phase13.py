import time
from contextlib import contextmanager


# ---------- Closures ----------

def make_multiplier(factor):
    def multiply(number):
        return number * factor  # "factor" is remembered from the outer function
    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)
print(f"Double 5: {double(5)}")
print(f"Triple 5: {triple(5)}")


# ---------- Decorators ----------
# A decorator wraps a function to add extra behavior, WITHOUT changing
# the original function's code. Decorators are built using closures.
def timer(func):
    """A decorator that measures and prints how long a function takes to run."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper


@timer
def process_data():
    total = sum(range(1_000_000))
    return total


print(f"Result: {process_data()}")


# A decorator that adds logging before/after a function runs
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper


@log_call
def add(a, b):
    return a + b


add(3, 4)


# ---------- Context Managers: __enter__ and __exit__ ----------
# "with" statements work because of two special methods: __enter__ (runs
# when entering the "with" block) and __exit__ (runs when leaving it,
# even if an error occurred).
class ManagedFile:
    """A custom context manager that mimics how 'open()' works internally."""

    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        print(f"Opening {self.filename}")
        self.file = open(self.filename, "w", encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()
        return False  # False means: don't suppress any exception that occurred


with ManagedFile("phase13_output.txt") as f:
    f.write("Written using a custom context manager.\n")


# ---------- contextlib: A Simpler Way to Write Context Managers ----------
@contextmanager
def timed_block(label):
    """Same idea as the timer decorator, but as a context manager instead."""
    start = time.time()
    yield  # code inside the "with" block runs here
    end = time.time()
    print(f"{label} took {end - start:.6f} seconds")


with timed_block("Summing numbers"):
    total = sum(range(500_000))


# ---------- Dunder Methods ----------
# "Dunder" = Double UNDERscore. These special methods let your custom
# classes work with Python's built-in syntax (print, len, ==, etc.).
class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        # Controls what shows up when you print() the object
        return f"Money({self.amount}, '{self.currency}')"

    def __len__(self):
        # Lets len() work on this object
        return int(self.amount)

    def __eq__(self, other):
        # Lets == work between two Money objects
        return self.amount == other.amount and self.currency == other.currency

    def __add__(self, other):
        # Lets + work between two Money objects
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies.")
        return Money(self.amount + other.amount, self.currency)


price_a = Money(100, "USD")
price_b = Money(50, "USD")

print(f"Repr: {price_a}")
print(f"Length: {len(price_a)}")
print(f"Equal? {price_a == Money(100, 'USD')}")
print(f"Sum: {price_a + price_b}")


# ---------- Descriptors/Properties (Conceptual) ----------
# A property lets a method be accessed like a plain attribute (no parentheses),
# while still running validation logic behind the scenes.
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is not possible.")
        self._celsius = value


temp = Temperature(25)
print(f"Initial temperature: {temp.celsius}")

temp.celsius = 30  # looks like a normal attribute assignment, but runs validation
print(f"Updated temperature: {temp.celsius}")

try:
    temp.celsius = -300  # this will raise an error via the setter's validation
except ValueError as exc:
    print(f"Caught expected error: {exc}")