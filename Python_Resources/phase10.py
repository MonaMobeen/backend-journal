"""
Phase 10: Debugging and Logging
Covers: reading tracebacks, breakpoint(), variable inspection, call stack,
structured logging, logging levels
"""

import logging

# ---------- Structured Logging Setup ----------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ---------- Logging Levels (from least to most severe) ----------
def demonstrate_logging_levels():
    logger.debug("DEBUG: Detailed info, useful only when diagnosing problems.")
    logger.info("INFO: Confirms things are working as expected.")
    logger.warning("WARNING: Something unexpected happened, but the program still works.")
    logger.error("ERROR: A serious problem - some functionality failed.")
    logger.critical("CRITICAL: A very serious error - the program may not continue.")


demonstrate_logging_levels()


# ---------- Reading Tracebacks ----------
# A traceback shows the exact chain of function calls that led to an error,
# read from TOP to BOTTOM, with the actual error type and message at the very end.
def divide(a, b):
    return a / b


def calculate_average_price(prices, quantity):
    total = sum(prices)
    return divide(total, quantity)   


def show_traceback_example():
    try:
        calculate_average_price([10, 20, 30], 0)
    except ZeroDivisionError:
        logger.exception("Caught an error - here is the full traceback:")
       


show_traceback_example()


# ---------- Using breakpoint() for Interactive Debugging ---------- 
def calculate_total(price, quantity):
    subtotal = price * quantity
    # breakpoint()  # <- uncomment this line to pause execution here
    tax = subtotal * 0.05
    return subtotal + tax


print(f"Total with tax: {calculate_total(100, 3)}")


# ---------- Variable Inspection and Call Stack (conceptual demonstration) ----------
def level_three():
    value = "deep in the call stack"
    # If you set a breakpoint here, the "call stack" would show:
    # level_three() was called by level_two(), which was called by level_one()
    return value


def level_two():
    return level_three()


def level_one():
    return level_two()


print(f"Call stack demo result: {level_one()}")


# ---------- Logging an Exception with Context ----------
def load_user_data(user_id):
    users = {1: "Memoona", 2: "Mobeen"}
    try:
        return users[user_id]
    except KeyError:
        logger.error("Failed to load user with id=%s - user not found.", user_id)
        return None


print(f"User lookup result: {load_user_data(99)}")


  