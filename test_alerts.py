# test_alerts.py
import alerts

# Fake data for testing
test_transactions = [
    {'category': 'Food', 'amount': 60},
    {'category': 'Food', 'amount': 40},
    {'category': 'Transport', 'amount': 20}
]

test_rules = [
    {'category': 'Food', 'threshold': 50},
    {'category': 'Transport', 'threshold': 40}
]

# Test the function
result = alerts.check_category_limits(test_transactions, test_rules)

for alert in result:
    print(alert)
