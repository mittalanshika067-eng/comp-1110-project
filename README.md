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

## File Structure 
comp-1110-project/
├── main.py              # Main program with text menu
├── transactions.py      # Transaction management (add, view, filter)
├── file_io.py           # File handling (save/load CSV and JSON)
├── stats.py             # Statistics calculations
├── alerts.py            # Alert system (budget checks)
├── data/                # Folder for data files
│   ├── transactions.csv # Saved transactions
│   ├── budget_rules.json # Budget rules
│   └── settings.json    # User settings (large transaction limit)
├── test_data/           # Sample test files
└── README.md

## Data file formats

1. transactions.csv: date,amount,category,description
eg. : 2026-04-09,70,Food,Lunch

2. budget_rules.json
eg. : 
