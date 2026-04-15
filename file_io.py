import json
import os


# Save all transactions to a file
# Each transaction is written as one line in CSV format: date,amount,category,description
def save_transactions(filename, transactions):
    try:
        # Get the folder name from the path (e.g., "data")
        folder = os.path.dirname(filename)

        # Create the folder if it does not exist
        if folder:
            os.makedirs(folder, exist_ok=True)

        # Open file in write mode (overwrites old data)
        with open(filename, "w", encoding="utf-8") as file:

            # Write each transaction as a line
            for t in transactions:
                line = (
                    t["date"] + "," +
                    str(t["amount"]) + "," +
                    t["category"] + "," +
                    t["description"] + "\n"
                )
                file.write(line)

    # Catch file errors or missing dictionary keys
    except (IOError, KeyError):
        print("Error saving transactions file")


# Load transactions from file into a list of dictionaries
def load_transactions(filename):

    transactions = []  # start with empty list

    try:
        # Open file in read mode
        with open(filename, "r", encoding="utf-8") as file:

            # Read file line by line
            for line in file:

                # Split line into values using commas
                parts = line.strip().split(",")

                # Skip lines that are not properly formatted
                if len(parts) != 4:
                    continue

                # Convert the text into a transaction dictionary
                transaction = {
                    "date": parts[0],
                    "amount": float(parts[1]),  # convert string to number
                    "category": parts[2],
                    "description": parts[3]
                }

                # Add transaction to list
                transactions.append(transaction)

    # File does not exist yet
    except FileNotFoundError:
        print("Transactions file not found")

    # Data inside file is invalid (e.g., amount not a number)
    except ValueError:
        print("Transactions file has invalid data")

    return transactions


# Save budget rules to a JSON file
# JSON is used because rules are structured data (list of dictionaries)
def save_rules(filename, rules):
    try:
        folder = os.path.dirname(filename)

        # Create folder if needed
        if folder:
            os.makedirs(folder, exist_ok=True)

        # Write rules list into file as JSON
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(rules, file, indent=4)

    except IOError:
        print("Error saving rules file")


# Load budget rules from JSON file
def load_rules(filename):
    try:
        # Read JSON file and convert to Python list
        with open(filename, "r", encoding="utf-8") as file:
            rules = json.load(file)

    # File does not exist yet
    except FileNotFoundError:
        print("Rules file not found")
        rules = []

    # File exists but JSON format is broken
    except json.JSONDecodeError:
        print("Rules file is corrupted")
        rules = []

    return rules


# Save list of categories to JSON file
def save_categories(filename, categories):
    try:
        folder = os.path.dirname(filename)

        # Create folder if needed
        if folder:
            os.makedirs(folder, exist_ok=True)

        # Save category list as JSON
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(categories, file, indent=4)

    except IOError:
        print("Error saving categories file")


# Load categories from JSON file
def load_categories(filename):
    try:
        # Read category list from file
        with open(filename, "r", encoding="utf-8") as file:
            categories = json.load(file)

    # File missing
    except FileNotFoundError:
        print("Categories file not found")
        categories = []

    # JSON broken
    except json.JSONDecodeError:
        print("Categories file is corrupted")
        categories = []

    return categories
