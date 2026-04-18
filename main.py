import transactions as t
import file_io as io
import stats as s
import alerts as a
from datetime import datetime

#load existing date and if that doesn't exist, create new data 
def load_or_create():

    transactions = io.load_transactions('data/transactions.csv') #path for required file
    if not transactions:
        transactions = []
        print("There are no existing transactions.")
    
    budget_rules = io.load_rules('data/budget_rules.json')
    if not budget_rules: 
        budget_rules = []
        print("There are no existing budgeting rules")

    return transactions, budget_rules

#save new or existing data 
def save_data(transactions, budget_rules):
    io.save_transactions('data/transactions.csv', transactions)
    io.save_rules('data/budget_rules.json', budget_rules)
    print("Data saved successfully!")

#ask user for large transaction limit once and then save it
def large_transaction_limit(budget_rules):

    #check if a limit already exists 
    for rules in budget_rules:             
        if rules.get("alert_type") == "large transaction":
            return rules.get('threshold', 300)
    
    #ask user for a limit ONE time
    print("Please enter a large transaction limit (for example $300)")
    
    try: 
        limit = input("Please enter a large transaction limit. The default limit is set at $300 hkd: ")
        if limit.strip() == "":
            limit = 300 
        else:
            limit = float(limit)
        
        budget_rules.append({
            'alert_type': 'large transaction',
            'threshold': limit
        })
        print(f"Large transaction limit set to ${limit}. Thank you")

        return limit
    
    except ValueError:
        print("Invalid input, the large transaction limit will be set to the default $300 hkd")

        budget_rules.append({'alert_type': 'large transaction', 'threshold' : 300})
        return 300



#shows full statistics report which only works if there are transactions.
def view_transactions():
    transactions = t.get_transactions()

    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n--- All Transactions ---")
    t.view_all()


def view_stats():
    transactions = t.get_transactions()

    if not transactions:
        print("\nNo transactions found yet. Please add some transactions to view full statistics")
        return

    s.print_full_statistics(transactions)


def check_alerts(budget_rules):
    transactions = t.get_transactions()

    if not transactions:
        print("\nNo transactions found. No alerts to display.")
        return

    print("Checking for alerts")
    all_alerts = a.run_all_alerts(transactions, budget_rules)

    if all_alerts:
        print(f"We found {len(all_alerts)} alert(s)")
        print()
        for alert in all_alerts:
            print(alert)
    else:
        print("Congratulations! No alerts found")

#edit any rules (add or remove)
def edit_budget_rules(budget_rules):

    print("Edit your budgeting rules")
    print("Current rules: ")

    if not budget_rules:
        print("No existing budgeting rules")

    else:
        for i,rule in enumerate(budget_rules): #loop through rule number and rule. i+1 because i starts from 0

            if rule.get('alert_type') == 'large transaction':
                print( f" {i+1}. Large transaction alert at > {rule.get('threshold', 300)}")

            elif rule.get('alert_type') == 'percentage':
                print(f"{i+1}. Percentage rule is : {rule.get('category', 'unknown')} > {rule.get('threshold', 0)}% of total spending")
            
            else:
                print(f"  {i+1}. {rule.get('category', 'Unknown')}: ${rule.get('threshold', 0)} ({rule.get('period', 'all time')}) - {rule.get('alert_type', 'category_cap')}")

    print("Here are the possible options to change your budget rules: ")
    print("  1. Add new category rule: ")
    print("  2. Add percentage rule: ")
    print("  3. Change large transaction limit: ")
    print("  4. Remove an existing rule: ")
    print("  5. Return to main menu: ")

    number = input('Please choose a number from 1-5 according to your needs: ')

    if number == '1':
        print('You have chosen to add a new category')

        category = input('Input a category: ')

        try: 
            threshold = float(input('Input amout limit for your category: '))
            period = input('Input a period (daily/weekly/monthly). If you want to view all time then press Enter: ')
            if period not in ['daily', 'weekly', 'monthly']:
                period = None
            
            budget_rules.append({
                'category': category,
                'threshold': threshold,
                'period': period,
                'alert_type': 'category_cap'
            })
            print(f"Rule added: {category} < ${threshold}")

        except ValueError:
            print("Invalid amount. Rule not added.")
    
    elif number == '2':
        print('You have chosen to add a new percentage rule')

        category = input("Enter category name: ")

        try:
            percentage = float(input("Enter percentage limit: "))

            budget_rules.append({
                'category': category,
                'threshold': percentage,
                'alert_type': 'percentage'
            })
            print(f"Percentage rule added: {category} > {percentage}% of total spending")
        except ValueError:
            print("Invalid percentage. Rule not added.")

    elif number == '3':
        print('You have decided to change your large transaction limit')

        try:
            limit = float(input("Enter new large transaction limit (HKD): "))
            # Remove existing large transaction rule
            budget_rules[:] = [r for r in budget_rules if r.get('alert_type') != 'large transaction'] #Create a new list with all rules except large transaction rules
            
            budget_rules.append({
                'alert_type': 'large transaction',
                'threshold': limit
            })

            print(f"Large transaction limit updated to ${limit}")

        except ValueError:
            print("Invalid amount. Limit not changed.")
    
    elif number == '4':
        print('You have chosen to delete a rule')
    
        try:
            rule_number = int(input("Enter rule number to delete: ")) - 1
            if 0 <= rule_number < len(budget_rules):
                removed = budget_rules.pop(rule_number)
                print(f"Removed rule: {removed}")

            else:
                print("Invalid rule number")

        except ValueError:
            print("Invalid input")

    elif number == '5':
        print('You have chosen to return to main menu')
    
    else:
        print('Invalid choice')

def main():
    
    print("-" * 40)
    print("   PERSONAL BUDGET ASSISTANT")
    print("-" * 40)
    print("Welcome to your personal budgeting tool!")
    
    # Load existing data
    transactions, budget_rules = load_or_create()

    t.transactions = transactions
    
    # Ask for large transaction limit if not set
    large_transaction_limit(budget_rules)
    
    # Main menu loop
    while True:
        print("\n" + "-" * 40)
        print("MAIN MENU")
        print()
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Statistics")
        print("4. Check Alerts")
        print("5. Edit Budget Rules")
        print("6. Save and Exit")
        
        choice = input("\nChoose an option (1-6): ")
        
        if choice == '1':
            t.add_transaction()
            transactions = t.get_transactions()
        
        elif choice == '2':
            view_transactions()
        
        elif choice == '3':
            view_stats()
        
        elif choice == '4':
            check_alerts(budget_rules)
        
        elif choice == '5':
            edit_budget_rules(budget_rules)
        
        elif choice == '6':
            save_data(transactions, budget_rules)
            print("Thank you for using Personal Budget Assistant!")
            break
        
        else:
            print("Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()
