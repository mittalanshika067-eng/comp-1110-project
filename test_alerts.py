# test_alerts.py
# test_alerts.py
import alerts

# Sample transactions for testing
test_transactions = [
    {'date': '2025-04-09', 'amount': 60, 'category': 'Food', 'description': 'Lunch'},
    {'date': '2025-04-09', 'amount': 20, 'category': 'Transport', 'description': 'MTR'},
    {'date': '2025-04-08', 'amount': 55, 'category': 'Food', 'description': 'Dinner'},
    {'date': '2025-04-07', 'amount': 50, 'category': 'Food', 'description': 'Lunch'},
    {'date': '2025-04-06', 'amount': 45, 'category': 'Food', 'description': 'Dinner'},
    {'date': '2025-04-05', 'amount': 40, 'category': 'Food', 'description': 'Lunch'},
    {'date': '2025-04-09', 'amount': 500, 'category': 'Shopping', 'description': 'New phone'},
    {'date': '2025-04-09', 'amount': 15, 'category': '', 'description': 'Snacks'},  # Uncategorized
]

# Sample budget rules
test_rules = [
    {'category': 'Food', 'threshold': 50, 'period': 'daily', 'alert_type': 'category_cap'},
    {'category': 'Food', 'threshold': 30, 'alert_type': 'percentage'},
    {'alert_type': 'large transaction', 'threshold': 300},
]

print("=" * 60)
print("TESTING ALERTS.PY")
print("=" * 60)

# Run all alerts
all_alerts = alerts.run_all_alerts(test_transactions, test_rules)

print(f"\nTotal alerts found: {len(all_alerts)}")
print("\n--- ALERTS ---")
for alert in all_alerts:
    print(alert)

if not all_alerts:
    print("No alerts triggered.")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
