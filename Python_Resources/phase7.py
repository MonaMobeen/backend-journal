import csv
import json
from pathlib import Path

# ---------- pathlib for File Paths ----------
 
data_dir = Path("phase7_data")
data_dir.mkdir(exist_ok=True)  # creates the folder if it doesn't already exist

text_path = data_dir / "notes.txt"
csv_path = data_dir / "users.csv"
json_path = data_dir / "config.json"
jsonl_path = data_dir / "events.jsonl"


# ---------- Context Managers and with open(...) ---------- 
def write_text_file():
    with text_path.open("w", encoding="utf-8") as file:
        file.write("Learning Python file handling.\n")
        file.write("This line was written using a context manager.\n")


def read_text_file():
    with text_path.open("r", encoding="utf-8") as file:
        content = file.read()
    print("---- Text file content ----")
    print(content)


write_text_file()
read_text_file()


# ---------- CSV ----------
def write_csv_file():
    rows = [
        {"name": "Minal", "role": "Frontend Developer"},
        {"name": "Mobeen", "role": "Backend Developer"},
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "role"])
        writer.writeheader()
        writer.writerows(rows)


def read_csv_file():
    print("---- CSV file content ----")
    with csv_path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)


write_csv_file()
read_csv_file()


# ---------- JSON ----------
def write_json_file():
    config = {"app_name": "PythonRoadmap", "version": 1, "debug": False}
    with json_path.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2)


def read_json_file():
    with json_path.open("r", encoding="utf-8") as file:
        config = json.load(file)
    print("---- JSON file content ----")
    print(config)


write_json_file()
read_json_file()


# ---------- JSONL (JSON Lines - one JSON object per line) ---------- 
def write_jsonl_file():
    events = [
        {"event": "login", "user": "mona"},
        {"event": "click", "user": "mona"},
        {"event": "logout", "user": "mona"},
    ]
    with jsonl_path.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event) + "\n")


def read_jsonl_file():
    print("---- JSONL file content (read line by line) ----")
    with jsonl_path.open("r", encoding="utf-8") as file:
        for line in file:
            event = json.loads(line)
            print(event)


write_jsonl_file()
read_jsonl_file()


# ---------- Encoding Awareness ---------- 
def encoding_example():
    text_with_special_chars = "Café, naïve, façade — testing UTF-8 support"
    special_path = data_dir / "encoding_demo.txt"
    with special_path.open("w", encoding="utf-8") as file:
        file.write(text_with_special_chars)

    with special_path.open("r", encoding="utf-8") as file:
        print("---- Encoding-aware read ----")
        print(file.read())


encoding_example() 

print("\nAll Phase 7 file operations completed. Covered 4 types of files: txt,csv,json,jsonl")