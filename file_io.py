import json
import os


def save_transactions(filename, transactions):
    try:
        folder = os.path.dirname(filename)
        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as file:
            for t in transactions:
                line = (
                    t["date"] + "," +
                    str(t["amount"]) + "," +
                    t["category"] + "," +
                    t["description"] + "\n"
                )
                file.write(line)

    except (IOError, KeyError):
        print("Error saving transactions file")


def load_transactions(filename):
    transactions = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")

                if len(parts) != 4:
                    continue

                transaction = {
                    "date": parts[0],
                    "amount": float(parts[1]),
                    "category": parts[2],
                    "description": parts[3]
                }

                transactions.append(transaction)

    except FileNotFoundError:
        print("Transactions file not found")

    except ValueError:
        print("Transactions file has invalid data")

    return transactions


def save_rules(filename, rules):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(rules, file, indent=4)

    except IOError:
        print("Error saving rules file")


def load_rules(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            rules = json.load(file)

    except FileNotFoundError:
        print("Rules file not found")
        rules = []

    except json.JSONDecodeError:
        print("Rules file is corrupted")
        rules = []

    return rules


def save_categories(filename, categories):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(categories, file, indent=4)

    except IOError:
        print("Error saving categories file")


def load_categories(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            categories = json.load(file)

    except FileNotFoundError:
        print("Categories file not found")
        categories = []

    except json.JSONDecodeError:
        print("Categories file is corrupted")
        categories = []

    return categories
