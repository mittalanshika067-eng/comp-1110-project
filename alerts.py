#check is limit for any category is exceeded 
#budget_rules: has list of rules with category and threshold in dictionary format
def check_category_limits(transactions, budget_rules):
   total_spending = {}                           #add total spending per category
   for transaction in transactions:
    category = transaction['category']
    amount = transaction['amount']

    if category in total_spending:                                  #once a category is in total_spending, amt will keep adding up
       total_spending[category] = total_spending[category] + amount

    else:
      total_spending[category] = amount

#total_spending will look like = { category : total_amount } 

#check budget rules per category 
    alerts = [] #list of alert messages 
    
    for rule in budget_rules:
       category = rule['category']
       limit = rule['threshold']

  #get how much was spent and see if limit exceeded
  #0 if category doesnt exist
       spending = total_spending.get(category, 0)
       if spending > limit:
          alert = f"WARNING: You spent ${spending} on {category}. The budget you set was ${limit}"
          alerts.append(alert)

   return alerts
