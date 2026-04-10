# COMP-1110-project- Personal Budgeting Assistant 

## Project Overview

Many university students in Hong Kong struggle to track daily expenses and by the end of the month, they often wonder where their money went. The problem is the lack of spending awareness.

Our Personal Budget Assistant solves this by providing a simple, text-based tool that helps students:
- **Track expenses** through manual entry or CSV import
- **Set budget rules** (e.g., "Food < $50/day")
- **Receive alerts** when overspending, making large purchases, or forgetting categories
- **View statistics** to understand spending patterns

The assistant is privacy-focused (no bank sync), easy to use, and designed specifically for student spending habits. It demonstrates computational thinking by modeling real-world budgeting as structured data (transactions, rules, alerts) processed through simple algorithms.

## Team Members and Contribution

- Krislyn Mariah Mendonca () - Transaction Management
- Miracle - File Handling
- Mansi - Summary Statistics
- Anshika Mittal (3036476023) - Alerts System & Menu Integration

## How to Run the Program

### Requirements
- Python 3.8 or higher
- No external libraries required (uses only standard library: datetime, csv, json, collections)

### Steps to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/comp1110-budget-assistant.git
   cd comp1110-budget-assistant

Running the program: python3 main.py


## Data file formats

1. transactions.csv: date,amount,category,description
- eg. : 2026-04-09,70,Food,Lunch

2. budget_rules.json
- eg. :[ {'category': 'Food', 'threshold': 50, 'period': 'daily', 'alert_type': 'category_cap'},
    {'category': 'Food', 'threshold': 30, 'alert_type': 'percentage'},
    {'alert_type': 'large transaction', 'threshold': 300} ] 

## Features 

Features

1. Transaction Management
- Add new transactions (date, amount, category, description)
- View all transactions
- Filter transactions by date or category

2. Budget Rules
- Set daily/weekly/monthly category spending limits
- Set percentage-based alerts (e.g., Food > 30% of total spending)
- Set large transaction alerts

3. Statistics
- Total spending
- Spending by category
- Daily/weekly/monthly breakdown
- Top spending categories
- Spending trends

4. Alerts
- Category cap exceeded (daily/weekly/monthly)
- Percentage of total spending exceeded
- Consecutive days overspending (3+ days)
- Large transaction detected
- Uncategorized transaction warning

## Sample Test Cases 
will add later

## Error Handling
- Missing files: Creates new files or uses defaults
- Corrupted JSON: Falls back to default settings
- Invalid input: Prompts user to re-enter correct values
- Empty transactions: Shows "No transactions found" message

## Limitations
- No automatic bank syncing (manual entry or CSV import only)
- No real-time spending tracking
- No multi-currency support
- Alerts are reactive (after spending), not proactive

## Future Improvements
- Add CSV import from banking apps
- Add spending predictions
- Add proactive alerts 
- Add mobile app version
