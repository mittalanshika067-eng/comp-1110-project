from datetime import datetime
from typing import List, Dict, Optional, Tuple
# Predefined categories for student spending
VALID_CATEGORIES = [
    "Food",
    "Transport", 
    "Coffee/Snacks",
    "Recreation",
    "School Supplies",
    "Bills",
    "Shopping",
    "Health",
    "Other"
]
transactions = []

# VALIDATION HELPER FUNCTIONS

def _validate_date(date_str: str) -> bool:
    """
    Check if date is in YYYY-MM-DD format and is a real date.
    Returns True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def _validate_amount(amount) -> bool:
    """
    Check if amount is a positive number.
    Returns True if valid, False otherwise.
    """
    try:
        amount_float = float(amount)
        return amount_float > 0 and amount_float < 1000000
    except (ValueError, TypeError):
        return False


def _validate_category(category: str) -> bool:
    """
    Check if category is in the valid categories list.
    Returns True if valid, False otherwise.
    """
    return category in VALID_CATEGORIES


def _validate_description(description: str) -> bool:
    """
    Check if description is not empty.
    Returns True if valid, False otherwise.
    """
    return description is not None and len(description.strip()) > 0

# USER INPUT FUNCTIONS

def get_valid_date_from_user() -> str:
    """
    Ask user for a date and keep asking until valid date is entered.
    
    Returns:
        Valid date string in YYYY-MM-DD format
    """
    while True:
        date_input = input("Enter date (YYYY-MM-DD): ").strip()
        
        if _validate_date(date_input):
            return date_input
        else:
            print("Error: Invalid date format. Please use YYYY-MM-DD (e.g., 2026-04-13)")


def get_valid_amount_from_user() -> float:
    """
    Ask user for an amount and keep asking until valid amount is entered.
    
    Returns:
        Valid positive amount as float
    """
    while True:
        try:
            amount_input = input("Enter amount (HKD): ").strip()
            amount_float = float(amount_input)
            
            if _validate_amount(amount_float):
                return round(amount_float, 2)
            else:
                print("Error: Amount must be a positive number (e.g., 45.50)")
        except ValueError:
            print("Error: Please enter a valid number")


def get_valid_category_from_user() -> str:
    """
    Display category menu and ask user to choose a category.
    Keep asking until valid category is selected.
    
    Returns:
        Valid category name string
    """
    display_categories()
    
    while True:
        try:
            choice = input("Select category (enter number or name): ").strip()
            
            # Check if input is a number
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(VALID_CATEGORIES):
                    return VALID_CATEGORIES[idx]
                else:
                    print(f"Error: Please enter a number between 1 and {len(VALID_CATEGORIES)}")
            else:
                # Check if input is a category name
                if choice in VALID_CATEGORIES:
                    return choice
                else:
                    print(f"Error: '{choice}' is not a valid category")
                    print(f"   Valid categories: {', '.join(VALID_CATEGORIES)}")
        except Exception:
            print("Error: Invalid input")


def get_valid_description_from_user() -> str:
    """
    Ask user for a description and keep asking until valid description is entered.
    
    Returns:
        Valid description string (not empty)
    """
    while True:
        description = input("Enter description: ").strip()
        
        if _validate_description(description):
            return description
        else:
            print("Error: Description cannot be empty")


def get_optional_notes_from_user() -> str:
    """
    Ask user for optional notes (can be empty).
    
    Returns:
        Notes string (can be empty)
    """
    notes = input("Enter notes (optional, press Enter to skip): ").strip()
    return notes


# MAIN FUNCTIONS

def add_transaction() -> List[Dict]:
    """
    Prompt user for transaction details and add to global transactions list.
    This function handles ALL user input for creating a transaction.
    
    Returns:
        The updated transactions list
    
    Example:
        transactions = add_transaction()
    """
    global transactions
    
    print("\n" + "-" * 50)
    print("ADD NEW TRANSACTION")
    print("-" * 50)
    
    # Get all inputs from user with validation
    date = get_valid_date_from_user()
    amount = get_valid_amount_from_user()
    category = get_valid_category_from_user()
    description = get_valid_description_from_user()
    notes = get_optional_notes_from_user()
    
    # Create transaction dictionary
    new_transaction = {
        "date": date,
        "amount": amount,
        "category": category,
        "description": description
    }
    
    # Add notes to transaction if provided
    if notes:
        new_transaction["notes"] = notes
    
    # Add to global list
    transactions.append(new_transaction)
    
    # Show success message
    print(f"\nTransaction added successfully!")
    print(f"   Date: {date}")
    print(f"   Amount: ${amount:.2f}")
    print(f"   Category: {category}")
    print(f"   Description: {description}")
    if notes:
        print(f"   Notes: {notes}")
    print("-" * 50)
    
    return transactions


def view_all() -> None:
    """
    Display all transactions in a readable format.
    Handles empty list by showing "No transactions found".
    Called by main.py when user selects view option.
    """
    global transactions
    
    if not transactions:
        print("\n" + "=" * 70)
        print("                    ALL TRANSACTIONS")
        print("=" * 70)
        print("\nNo transactions found.")
        print("Please add some transactions using option 1.")
        print("\n" + "=" * 70 + "\n")
        return
    
    # Calculate total spending for summary
    total_spending = sum(t['amount'] for t in transactions)
    
    print("\n" + "=" * 70)
    print("                    ALL TRANSACTIONS")
    print("=" * 70)
    
    # Display each transaction with index number
    for i, t in enumerate(transactions, 1):
        # Basic display without notes
        display_line = f"  {i:2}. {t['date']} | ${t['amount']:>8.2f} | {t['category']:<15} | {t['description']}"
        
        # Add notes if they exist
        if 'notes' in t and t['notes']:
            display_line += f" | Notes: {t['notes']}"
        
        print(display_line)
    
    print("-" * 70)
    print(f"  Total transactions: {len(transactions)}")
    print(f"  Total spending: ${total_spending:.2f}")
    print("=" * 70 + "\n")


def get_transactions() -> List[Dict]:
    """
    Return the current transactions list.
    Used by other modules (statistics.py, alerts.py, file_handler.py) to access data.
    
    Returns:
        The global transactions list
    
    Example:
        all_transactions = get_transactions()
    """
    global transactions
    return transactions

# OPTIONAL FILTER FUNCTIONS 

def filter_by_date(transaction_list: List[Dict], start_date: str, end_date: str) -> List[Dict]:
    """
    Filter transactions between two dates (inclusive).
    
    Parameters:
        transaction_list: List of transaction dictionaries
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        List of transactions within the date range
    
    Example:
        march_transactions = filter_by_date(transactions, "2026-03-01", "2026-03-31")
    """
    filtered = []
    
    for t in transaction_list:
        if start_date <= t['date'] <= end_date:
            filtered.append(t)
    
    return filtered


def filter_by_category(transaction_list: List[Dict], category: str) -> List[Dict]:
    """
    Filter transactions by category.
    
    Parameters:
        transaction_list: List of transaction dictionaries
        category: Category name (must be in VALID_CATEGORIES)
    
    Returns:
        List of transactions matching the category
    
    Example:
        food_transactions = filter_by_category(transactions, "Food")
    """
    filtered = []
    
    for t in transaction_list:
        if t['category'] == category:
            filtered.append(t)
    
    return filtered


def filter_by_date_range(transaction_list: List[Dict], start_date: str = None, end_date: str = None) -> List[Dict]:
    """
    Filter transactions by date range with optional start/end.
    More flexible version of filter_by_date.
    
    Parameters:
        transaction_list: List of transaction dictionaries
        start_date: Start date (optional, None means no lower bound)
        end_date: End date (optional, None means no upper bound)
    
    Returns:
        List of transactions within the date range
    """
    filtered = transaction_list.copy()
    
    if start_date:
        filtered = [t for t in filtered if t['date'] >= start_date]
    
    if end_date:
        filtered = [t for t in filtered if t['date'] <= end_date]
    
    return filtered


def get_category_list() -> List[str]:
    """
    Return the list of valid categories.
    Used by main.py to display category menu.
    
    Returns:
        List of category names
    """
    return VALID_CATEGORIES.copy()


def display_categories() -> None:
    """
    Display all available categories.
    Used by main.py to show user what categories they can choose.
    """
    print("\nAvailable Categories:")
    print("   " + "-" * 35)
    for i, cat in enumerate(VALID_CATEGORIES, 1):
        print(f"   {i:2}. {cat}")
    print("   " + "-" * 35)


def get_transaction_count() -> int:
    """
    Return the number of transactions.
    Used for statistics and validation.
    
    Returns:
        Number of transactions in the global list
    """
    global transactions
    return len(transactions)


def get_total_spending() -> float:
    """
    Calculate total spending from all transactions.
    
    Returns:
        Total spending amount
    """
    global transactions
    return sum(t['amount'] for t in transactions)


def get_last_transaction() -> Optional[Dict]:
    """
    Get the most recently added transaction.
    
    Returns:
        Last transaction dictionary, or None if no transactions exist
    """
    global transactions
    if transactions:
        return transactions[-1]
    return None


def clear_all_transactions() -> None:
    """
    Remove all transactions from the global list.
    Used for testing or resetting data.
    """
    global transactions
    transactions.clear()
    print("All transactions have been cleared.")

# FOR INTEGRATION WITH OTHER MODULES

"""
HOW OTHER MODULES USE THIS FILE:

1. statistics.py expects:
   - get_transactions() to get the list
   - Each transaction has 'date', 'amount', 'category', 'description'

2. alerts.py expects:
   - get_transactions() to get the list
   - Each transaction has 'date', 'amount', 'category'

3. file_handler.py expects:
   - get_transactions() to get the list for saving
   - add_transaction() is NOT used by file_handler (it loads directly)
   
4. main.py expects:
   - add_transaction() to add new transactions (with user input inside)
   - view_all() to display transactions
   - get_transactions() to pass to other modules
   - get_category_list() for category menu
   - display_categories() for showing options
"""


# SELF-TEST 

if __name__ == "__main__":
    """
    This section runs when you execute: python transactions.py
    It allows you to test the module interactively.
    """
    print("\n" + "=" * 60)
    print("TRANSACTIONS MODULE - INTERACTIVE TEST")
    print("=" * 60)
    print("\nThis is a test of the transactions module.")
    print("You can add transactions and view them.")
    
    while True:
        print("\n" + "-" * 40)
        print("TEST MENU")
        print("-" * 40)
        print("1. Add a transaction")
        print("2. View all transactions")
        print("3. Clear all transactions")
        print("4. Exit test")
        print("-" * 40)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            add_transaction()
        
        elif choice == "2":
            view_all()
        
        elif choice == "3":
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm == "yes":
                clear_all_transactions()
            else:
                print("Cancelled.")
        
        elif choice == "4":
            print("\nExiting test. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    print("\n" + "=" * 60)
    print("Test completed")
    print("=" * 60)
