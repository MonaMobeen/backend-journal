import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------- try / except / else / finally ----------
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: cannot divide by zero.")
        return None
    else:
        # 'else' runs ONLY if no exception occurred in the try block
        print("Division succeeded.")
        return result
    finally:
        # 'finally' ALWAYS runs, whether there was an error or not
        print("Division attempt finished.\n")


divide(10, 2)
divide(10, 0)


# ---------- raise ----------
def check_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative.")
    return age


try:
    check_age(-5)
except ValueError as exc:
    print(f"Caught raised error: {exc}\n")


# ---------- Built-in Exception Types ----------
def demonstrate_builtin_exceptions():
    examples = []

    try:
        int("not a number")
    except ValueError as exc:
        examples.append(f"ValueError: {exc}")

    try:
        [1, 2, 3][10]
    except IndexError as exc:
        examples.append(f"IndexError: {exc}")

    try:
        {"a": 1}["b"]
    except KeyError as exc:
        examples.append(f"KeyError: {exc}")

    try:
        None.some_method()
    except AttributeError as exc:
        examples.append(f"AttributeError: {exc}")

    for example in examples:
        print(example)
    print()


demonstrate_builtin_exceptions()


# ---------- Catching Specific Exceptions (never a bare except) ----------
def safe_divide(a, b):
    try:
        return a / b
    except (ZeroDivisionError, TypeError) as exc:
        # Catching SPECIFIC exceptions is better than a bare "except:"
        # A bare except can hide real bugs and makes debugging much harder.
        print(f"Handled specific error: {exc}")
        return None


safe_divide(10, 0)
safe_divide(10, "a")
print()


# ---------- Custom Exceptions ----------
class InsufficientFundsError(Exception):
    """Custom exception for domain-specific error cases."""

    def __init__(self, balance, amount):
        message = f"Cannot withdraw {amount}, balance is only {balance}."
        super().__init__(message)
        self.balance = balance
        self.amount = amount


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


try:
    withdraw(100, 500)
except InsufficientFundsError as exc:
    print(f"Custom exception caught: {exc}\n")


# ---------- Exception Propagation ----------
def inner_function():
    raise RuntimeError("Something went wrong deep inside.")


def middle_function():
    inner_function()  # error is not caught here - it propagates upward


def outer_function():
    try:
        middle_function()
    except RuntimeError as exc:
        # The exception "bubbled up" through middle_function to here
        print(f"Caught propagated exception: {exc}\n")


outer_function()


# ---------- Logging an Exception ----------
def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as exc:
        logger.error("Input file missing: %s", exc)
        return None


process_file("this_file_does_not_exist.txt")


# ---------- When to Handle vs Re-raise ----------
def load_config(path):
    """
    Sometimes you can't fully handle an error at this level - you log it
    for context, then re-raise so a higher level can decide what to do
    (e.g. show a user-friendly message or exit the program).
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logger.error("Config file not found at %s", path)
        raise  # re-raise: this function isn't the right place to fully recover


try:
    load_config("missing_config.txt")
except FileNotFoundError:
    print("Handled at a higher level: falling back to default configuration.")

 