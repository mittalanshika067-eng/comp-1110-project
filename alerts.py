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
    
    alerts = [] #empty dict to store neccesary alerts
    
    for rule in budget_rules:
        category = rule['category']
        limit = rule['threshold']
        period = rule.get('period')

   #find the relevant transaction
    if period == 'daily':
        period_transaction = check_by_time(transactions,'daily')
    elif period == 'weekly':
        period_transaction = check_by_time(transactions,'weekly')
    elif period == 'monthly':
        period_transaction = check_by_time(transactions,'monthly')
    else:
        period_transaction = transactions 


    total_spending = 0 #add up spending per category
    for i in period_transaction:
        if i['category'] == category:
            total_spending += i['amount']
    
    if total_spending > limit:
        alert = f"Warning: You spent ${total_spending:.2f} on {category}. Your budget was ${limit}"
        alerts.append(alert)

    return alerts


    





