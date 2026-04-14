import json  # lets us save/load data in JSON format

# Save transactions to a file (CSV-style text)
def save_transactions(filename, transactions):

    # open file in write mode ("w") — this creates or overwrites the file
    with open(filename, "w") as file:

        # go through each transaction in the list
        for t in transactions:

            # create one line of text separated by commas
            line = (
                t["date"] +
                "," +
                str(t["amount"]) +
                "," +
                t["category"] +
                "," +
                t["description"] +
                "\n"
            )

            # write that line into the file
            file.write(line)


# Load transactions from a file
def load_transactions(filename):

    transactions = []  # empty list to store results

    try:

        # open file in read mode
        with open(filename, "r") as file:

            # read each line
            for line in file:

                # split the line into parts using commas
                parts = line.strip().split(",")

                # skip bad lines that don't have 4 values
                if len(parts) != 4:
                    continue

                # create dictionary from the parts
                transaction = {
                    "date": parts[0],
                    "amount": float(parts[1]),  # convert text to number
                    "category": parts[2],
                    "description": parts[3]
                }

                # add it to the list
                transactions.append(transaction)

    except FileNotFoundError:

        # if file doesn't exist
        print("File not found")

    return transactions


# Save rules to a JSON file
def save_rules(filename, rules):

    try:

        # open file in write mode
        with open(filename, "w") as file:

            # write dictionary into file as JSON
            json.dump(rules, file, indent=4)

    except IOError:

        print("Error saving rules file")


# Load rules from a JSON file
def load_rules(filename):

    try:

        # open file in read mode
        with open(filename, "r") as file:

            # read JSON and convert it into a dictionary
            rules = json.load(file)

    except FileNotFoundError:

        print("Rules file not found")
        rules = []

    except json.JSONDecodeError:

        print("Rules file is corrupted")
        rules = []

    return rules
