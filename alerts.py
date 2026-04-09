# alerts.py
# This file checks for budget violations and generates warning messages

from datetime import datetime, timedelta
from collections import defaultdict

# Filter transactions by time period. Time period can be: "daily" (today), "weekly" (last 7 days), "monthly" (this month), or "all"
def check_by_time(transactions, period):

    today = datetime.now().date()
    filtered_data = []

    for transaction in transactions:
        transaction_date = datetime.strptime(transaction['date'], "%Y-%m-%d").date()   #Converts the transaction's date string (like "2025-04-08") into a date object 

        if period == "daily":
            if transaction_date == today:
                filtered_data.append(transaction)

        elif period == "weekly":
            if transaction_date >= today - timedelta(days=7):       #checks if date is within the past week (today - last 7 days)
                filtered_data.append(transaction)

        elif period == "monthly":
            if transaction_date.year == today.year and transaction_date.month == today.month: #checks the past year - month AND year has to be the same
                filtered_data.append(transaction)

        else:
            filtered_data.append(transaction)

    return filtered_data


#check is limit for any category is exceeded 
#budget_rules: has list of rules with category and threshold in dictionary format
def check_category_limits(transactions, budget_rules):

    alerts = []  #empty list to store necessary alerts

    for rule in budget_rules:

        if 'category' not in rule:
            continue
        if rule.get('alert_type') == 'percentage':
            continue

        category = rule['category']
        limit = rule['threshold']
        period = rule.get('period')

        #find the relevant transaction
        if period == 'daily':
            period_transaction = check_by_time(transactions, 'daily')
        elif period == 'weekly':
            period_transaction = check_by_time(transactions, 'weekly')
        elif period == 'monthly':
            period_transaction = check_by_time(transactions, 'monthly')
        else:
            period_transaction = transactions

        total_spending = 0  #add up spending per category
        for i in period_transaction:
            if i['category'] == category:
                total_spending += i['amount']

        if total_spending > limit:
            alert = f"Warning: You spent ${total_spending:.2f} on {category}. Your budget was ${limit}"
            alerts.append(alert)

    return alerts


# Check if any category exceeds the threshold percentage of spending
# For percentage alerts, 'threshold' means PERCENTAGE NOT spending ($/money)
def check_percentage_alerts(transactions, budget_rules):

    alerts = []

    # Calculate total spending to then help calculate percentages
    total_spending = 0
    for i in transactions:
        total_spending += i['amount']

    # If no spending at all, return empty list 
    if total_spending == 0:
        return alerts

    # Calculate spending for each category and store it as a dictionary {category:amount}
    category_totals = {}
    for transaction in transactions:
        category = transaction['category']
        amount = transaction['amount']

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    # Check only that rule that is a percentage rule, if not skip 
    for rule in budget_rules:
        if rule.get('alert_type') != 'percentage':
            continue

        category = rule['category']
        percentage_limit = rule['threshold']  # For percentage rules, 'threshold' means % not the same as spending in above function

        # Get amount spent on this category (0 if none)
        if category in category_totals:
            spent = category_totals[category]
        else:
            spent = 0

        # Calculate actual percentage of total spending
        actual_percentage = (spent / total_spending) * 100

        if actual_percentage > percentage_limit:
            alert = f"Warning: {category} is {actual_percentage:.1f}% of your spending. Limit was {percentage_limit}%"
            alerts.append(alert)

    return alerts


#check categorized that are not categorized properly 
def check_uncategorized(transactions):
    alerts = []

    for i in transactions:
        category = i.get('category')

        #if category is None or empty string or uncategorized
        if not category or category.lower() == 'uncategorized':
            alert = f"Warning: Uncategorized: ${i['amount']} on {i['date']} - Please add a category"
            alerts.append(alert)

    return alerts


def check_overspending(transactions, budget_rules):
    alerts = []

    if not transactions:
        return alerts

    #Organize spending by date and category
    #Date is a key, and the value is another dictionary (which contains category-amount pairs)- nested dictionary
    daily_spending = {}

    for i in transactions:
        date = i['date']
        category = i['category']
        amount = i['amount']

        if date not in daily_spending:
            daily_spending[date] = {}

        #if category not found in the date's dictionary start with 0
        if category not in daily_spending[date]:
            daily_spending[date][category] = 0

        #get date based category and respective spending
        daily_spending[date][category] += amount

    sorted_dates = sorted(daily_spending.keys())

    # Check each rule that has a daily period
    for rule in budget_rules:
        if rule.get('period') != 'daily':
            continue

        category = rule['category']
        limit = rule['threshold']

        consecutive_days = 0  # Counter for how many days in a row over budget

        for date in sorted_dates:
            # Check if category exists for this date
            if category in daily_spending[date]:
                spent = daily_spending[date][category]
            else:
                spent = 0

            if spent > limit:
                consecutive_days += 1
            else:
                if consecutive_days >= 3:
                    alert = f"Warning: Overspent on {category} for {consecutive_days} number of days in a row"
                    alerts.append(alert)
                consecutive_days = 0  #reset counter after non overspending day 

        if consecutive_days >= 3:
            alert = f"Warning: Overspent on {category} for {consecutive_days} number of days in a row"
            alerts.append(alert)

    return alerts


def large_transaction(transactions, budget_rules):
    alerts = []

    #check the rule for large transaction 
    large_amount_limit = 300  #default large amount
    for rule in budget_rules:
        if rule.get('alert_type') == 'large transaction':
            large_amount_limit = rule.get('threshold', 300)

    for i in transactions:
        if i['amount'] > large_amount_limit:
            alert = f"Warning: You have exceeded your limit of {large_amount_limit} on {i['category']} on {i['date']}. Your spending was ${i['amount']}"
            alerts.append(alert)

    return alerts


#Run all alert checks and return combined alerts. alerts.extend() is used to append more than one item since append can only add 1 at a time.
def run_all_alerts(transactions, budget_rules):
    all_alerts = []

    # 1. Category limit alerts (daily/weekly/monthly caps)
    limit_alerts = check_category_limits(transactions, budget_rules)
    all_alerts.extend(limit_alerts)

    # 2. Percentage alerts 
    percent_alerts = check_percentage_alerts(transactions, budget_rules)
    all_alerts.extend(percent_alerts)

    # 3. Consecutive overspend alerts
    overspend_alerts = check_overspending(transactions, budget_rules)
    all_alerts.extend(overspend_alerts)

    # 4. Large transaction alerts
    large_alerts = large_transaction(transactions, budget_rules)
    all_alerts.extend(large_alerts)

    # 5. Uncategorized alerts
    uncategorized_alerts = check_uncategorized(transactions)
    all_alerts.extend(uncategorized_alerts)

    return all_alerts
