import csv
import json
from pathlib import Path


# ---------- Sample Data Setup ----------

SALES_CSV = Path("sales.csv")
SALES_JSONL = Path("sales.jsonl")

sample_rows = [
    {"id": 1, "product": "Laptop", "city": "Lahore", "amount": 1200},
    {"id": 2, "product": "Mouse", "city": "Karachi", "amount": 20},
    {"id": 3, "product": "Laptop", "city": "Karachi", "amount": 1100},
    {"id": 4, "product": "Keyboard", "city": "Lahore", "amount": 50},
    {"id": 5, "product": "Monitor", "city": "Islamabad", "amount": 300},
]


def create_sample_csv():
    with SALES_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "product", "city", "amount"])
        writer.writeheader()
        writer.writerows(sample_rows)


# ---------- Working with CSV ----------

def read_csv_all():
    """Reads the whole file into memory at once - fine for small files."""
    with SALES_CSV.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def read_csv_row_by_row():
    """
    Reads one row at a time instead of loading everything into memory.
    This matters a lot once the file has millions of rows - you only
    ever hold ONE row in memory instead of the whole file.
    """
    with SALES_CSV.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row   # yield = "hand over one row, then pause here"


# ---------- Filtering and Grouping (plain Python, no libraries) ----------

def filter_by_city(rows, city: str):
    return [row for row in rows if row["city"] == city]


def group_total_by_product(rows):
    """
    Groups rows by 'product' and sums the 'amount' for each group.
    This is the same idea as Excel's PivotTable / SUMIF.
    """
    totals = {}
    for row in rows:
        product = row["product"]
        amount = int(row["amount"])
        totals[product] = totals.get(product, 0) + amount
    return totals


# ---------- Converting CSV -> JSON Lines (JSONL) ----------

# JSON Lines (.jsonl) = one JSON object per line. Useful for large
# datasets because you can process line-by-line instead of loading
# one giant JSON array into memory.

def convert_csv_to_jsonl():
    rows = read_csv_all()
    with SALES_JSONL.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row) + "\n")


def read_jsonl_row_by_row():
    with SALES_JSONL.open("r", encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)


# ---------- Chunking (processing large files in pieces) ----------

def process_in_chunks(rows, chunk_size: int = 2):
    """
    Instead of processing 1 row or ALL rows at once, process a small
    batch ("chunk") at a time. Useful when a single row is too small
    to be efficient, but loading everything is too much memory.
    """
    chunk = []
    for row in rows:
        chunk.append(row)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:  # leftover rows smaller than a full chunk
        yield chunk


# ---------- Running the Plain-Python Demo ----------

def run_plain_python_demo():
    create_sample_csv()

    print("All rows (loaded at once):")
    print(read_csv_all())

    print("\nRow-by-row (generator, memory-friendly):")
    for row in read_csv_row_by_row():
        print(row)

    print("\nFiltered - only Lahore:")
    print(filter_by_city(read_csv_all(), "Lahore"))

    print("\nGrouped totals by product:")
    print(group_total_by_product(read_csv_all()))

    convert_csv_to_jsonl()
    print("\nConverted to JSONL, reading it back:")
    for record in read_jsonl_row_by_row():
        print(record)

    print("\nProcessing in chunks of 2:")
    for chunk in process_in_chunks(read_csv_all(), chunk_size=2):
        print(chunk)


# ---------- Pandas / NumPy  ----------

# Pandas gives you a "DataFrame" - think of it as a smart, programmable
# spreadsheet. NumPy gives you fast arrays for numeric work. Neither is
# required - plain Python (above) can do the same things, just with more
# manual code. Pandas/NumPy just make it shorter and faster for big data.

def run_pandas_demo():
    import pandas as pd
    import numpy as np

    df = pd.read_csv(SALES_CSV)   # loads the whole CSV into a DataFrame

    print("\nDataFrame preview:")
    print(df)

    print("\nFilter - only Lahore rows:")
    print(df[df["city"] == "Lahore"])

    print("\nGroup and sum by product (same result as our manual function):")
    print(df.groupby("product")["amount"].sum())

    # A quick NumPy example: turn the 'amount' column into a NumPy array
    amounts = np.array(df["amount"])
    print("\nAverage amount (NumPy):", amounts.mean())


if __name__ == "__main__":
    run_plain_python_demo()
    

 