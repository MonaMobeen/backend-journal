numbers = [1, 2, 3]

# Turning it into an "iterator" using iter()
numbers_iterator = iter(numbers)

# ---------- iter() and next() ----------
print(next(numbers_iterator))  # 1
print(next(numbers_iterator))  # 2
print(next(numbers_iterator))  # 3

# ---------- StopIteration ----------
try:
    print(next(numbers_iterator))  # no items left
except StopIteration:
    print("No more items in the iterator (StopIteration raised).")

# ---------- How a for-loop uses an iterator internally ----------
# This is what a for-loop is doing behind the scenes:
manual_list = [10, 20, 30]
manual_iterator = iter(manual_list)
while True:
    try:
        item = next(manual_iterator)
        print(f"Manual iteration item: {item}")
    except StopIteration:
        break

# ---------- Generator Functions and yield ----------
def count_up_to(limit):
    number = 1
    while number <= limit:
        yield number
        number += 1

print("Generator function output:")
for value in count_up_to(5):
    print(value)

# ---------- Generator Expressions ----------
squares_generator = (n ** 2 for n in range(5))
print("Generator expression output:")
for square in squares_generator:
    print(square)

# ---------- Lazy Evaluation Demonstration ----------
def read_numbers(limit):
    for number in range(limit):
        yield number  # values are produced one at a time, not all at once

# Only a small amount of memory is used even for a huge range
lazy_numbers = read_numbers(1_000_000)
first_five = [next(lazy_numbers) for _ in range(5)]
print(f"First five lazy numbers: {first_five}")

# ---------- List vs Generator: Key Comparison ----------
list_version = [n for n in range(5)]        # all values created immediately
generator_version = (n for n in range(5))   # values created only when requested
print(f"List version (materialized): {list_version}")
print(f"Generator version (lazy object): {generator_version}")
print(f"Generator values when consumed: {list(generator_version)}")

# ---------- Processing Large Files Line by Line (example pattern) ----------
def process_large_file(file_path):
    """
    Demonstrates reading a file line by line using a generator,
    instead of loading the entire file into memory at once.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            yield line.strip()

# Create a small sample file to demonstrate the pattern
sample_file_path = "sample_data.txt"
with open(sample_file_path, "w", encoding="utf-8") as sample_file:
    sample_file.write("line one\nline two\nline three\n")

print("Processing file line by line using a generator:")
for processed_line in process_large_file(sample_file_path):
    print(processed_line)

# ---------- Chunk-Based Processing (streaming records pattern) ----------
def chunk_data(data, chunk_size):
    """Yield successive chunks from a list, one chunk at a time."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

sample_data = list(range(10))
print("Chunk-based processing output:")
for chunk in chunk_data(sample_data, 3):
    print(chunk)