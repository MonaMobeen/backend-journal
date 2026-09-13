from dataclasses import dataclass


# ---------- Constants Instead of Magic Values ----------
# BAD: using unexplained raw numbers ("magic values") scattered in the code
# if age >= 18: ...
#
# GOOD: give the number a meaningful name, defined once at the top
ADULT_AGE = 18
DISCOUNT_RATE = 0.10
MAX_LOGIN_ATTEMPTS = 3


# ---------- Meaningful Names ----------
# BAD naming (avoid this):
# def f(x, y):
#     return x * y * 0.1

# GOOD naming - the function and parameters explain themselves
def calculate_discounted_price(price: float, quantity: int) -> float:
    """Return the total price after applying the standard discount rate."""
    subtotal = price * quantity
    return subtotal * (1 - DISCOUNT_RATE)


print(f"Discounted price: {calculate_discounted_price(100, 2)}")


# ---------- Small, Focused Functions (Single Responsibility) ----------
# BAD: one function doing too many unrelated things at once
# def process_order(order):
#     validate(order)
#     calculate_total(order)
#     save_to_database(order)
#     send_email(order)
#     print("Done")
#
# GOOD: each function does ONE clear job, and a coordinating function calls them
def validate_order(order: dict) -> bool:
    """Checks that an order has the minimum required fields."""
    return "item" in order and "quantity" in order


def calculate_order_total(order: dict, unit_price: float) -> float:
    """Calculates the total cost for an order."""
    return unit_price * order["quantity"]


def process_order(order: dict, unit_price: float) -> float:
    """
    Coordinates the steps needed to process an order.
    Notice this function is short and readable - it delegates the real
    work to smaller, single-purpose functions instead of doing everything itself.
    """
    if not validate_order(order):
        raise ValueError("Invalid order: missing required fields.")
    return calculate_order_total(order, unit_price)


sample_order = {"item": "Book", "quantity": 3}
print(f"Order total: {process_order(sample_order, unit_price=15)}")


# ---------- Avoiding Duplication (DRY - Don't Repeat Yourself) ----------
# BAD: the same calculation copy-pasted in multiple places
# tax_a = price_a * 0.05
# tax_b = price_b * 0.05
# tax_c = price_c * 0.05
#
# GOOD: write the logic once, reuse it everywhere
TAX_RATE = 0.05


def calculate_tax(price: float) -> float:
    """Calculates tax for a given price using the standard tax rate."""
    return price * TAX_RATE


for item_price in [100, 250, 40]:
    print(f"Price: {item_price}, Tax: {calculate_tax(item_price)}")


# ---------- Type Hints and Useful Docstrings ----------
def find_average(numbers: list[float]) -> float:
    """
    Calculate the average of a list of numbers.

    Args:
        numbers: A list of numeric values. Must not be empty.

    Returns:
        The arithmetic mean of the provided numbers.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate average of an empty list.")
    return sum(numbers) / len(numbers)


print(f"Average: {find_average([10, 20, 30])}")


# ---------- Separation of Concerns ----------
# Each of these functions has ONE job: extract, validate, transform, save.
# This mirrors a common data-pipeline pattern:
#   extract() -> validate() -> transform() -> save()
def extract(raw_data: str) -> list[str]:
    """Splits raw comma-separated text into individual items."""
    return raw_data.split(",")


def validate(items: list[str]) -> list[str]:
    """Removes empty or whitespace-only items."""
    return [item.strip() for item in items if item.strip()]


def transform(items: list[str]) -> list[str]:
    """Converts all items to title case."""
    return [item.title() for item in items]


def save(items: list[str]) -> None:
    """Simulates saving the final, cleaned data."""
    print(f"Saved items: {items}")


def run_pipeline(raw_data: str) -> None:
    items = extract(raw_data)
    items = validate(items)
    items = transform(items)
    save(items)


run_pipeline("mona, sana,, sara ,  ")


# ---------- Avoiding Deeply Nested Logic ----------
# BAD: deeply nested if-statements are hard to read and follow
def check_eligibility_bad(age, has_id, has_ticket):
    if age >= ADULT_AGE:
        if has_id:
            if has_ticket:
                return "Entry allowed"
            else:
                return "No ticket"
        else:
            return "No ID"
    else:
        return "Underage"


# GOOD: use "early returns" (guard clauses) to flatten the logic
def check_eligibility_good(age: int, has_id: bool, has_ticket: bool) -> str:
    """Determines entry eligibility using early returns instead of deep nesting."""
    if age < ADULT_AGE:
        return "Underage"
    if not has_id:
        return "No ID"
    if not has_ticket:
        return "No ticket"
    return "Entry allowed"


print(check_eligibility_good(20, True, True))


# ---------- Dataclasses Keep Data Definitions Clean ----------
@dataclass
class Product:
    name: str
    price: float
    quantity: int

    def total_price(self) -> float:
        return self.price * self.quantity


product = Product(name="Notebook", price=5.5, quantity=4)
print(f"Product total: {product.total_price()}")

 