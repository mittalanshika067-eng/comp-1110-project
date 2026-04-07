from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple, Optional


def get_total_spending(transactions: List[Dict]) -> float:
    """Calculate total spending from all transactions."""
    total = 0.0
    for transaction in transactions:
        total += transaction['amount']
    return round(total, 2)


def get_category_breakdown(transactions: List[Dict]) -> Dict[str, float]:
    """Calculate spending breakdown by category."""
    breakdown = defaultdict(float)
    
    for transaction in transactions:
        category = transaction['category']
        breakdown[category] += transaction['amount']
    
    for category in breakdown:
        breakdown[category] = round(breakdown[category], 2)
    
    return dict(breakdown)


def get_time_based_summary(transactions: List[Dict], period: str = "monthly") -> Dict[str, float]:
    """
    Get spending summary grouped by time period.
    period can be "daily", "weekly", or "monthly"
    """
    summary = defaultdict(float)
    
    for transaction in transactions:
        date_str = transaction['date']
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        amount = transaction['amount']
        
        if period == "daily":
            key = date_str
        elif period == "weekly":
            # isocalendar() returns (year, week_number, weekday)
            year, week, _ = date_obj.isocalendar()
            key = f"{year}-W{week:02d}"  # Format: "2024-W11" for week 11
        elif period == "monthly":
            key = date_obj.strftime("%Y-%m")  # Format: "2024-03" for March 2024
        else:
            raise ValueError("Period must be 'daily', 'weekly', or 'monthly'")
        
        summary[key] += amount
    
    for key in summary:
        summary[key] = round(summary[key], 2)
    
    return dict(summary)


def get_top_categories(transactions: List[Dict], top_n: int = 3) -> List[Tuple[str, float]]:
    """Find the top spending categories."""
    breakdown = get_category_breakdown(transactions)
    # Sort by amount (second item in tuple) from highest to lowest
    sorted_categories = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
    return sorted_categories[:top_n]


def get_spending_trend(transactions: List[Dict]) -> Dict:
    """Analyze spending trends over time."""
    if not transactions:
        return {
            "trend": "No data available", 
            "average_daily_spending": 0, 
            "highest_spending_day": None,
            "highest_spending_amount": 0
        }
    
    daily_spending = get_time_based_summary(transactions, "daily")
    
    if not daily_spending:
        return {
            "trend": "No data available", 
            "average_daily_spending": 0, 
            "highest_spending_day": None,
            "highest_spending_amount": 0
        }
    
    total_days = len(daily_spending)
    total_spent = sum(daily_spending.values())
    average_daily = total_spent / total_days if total_days > 0 else 0
    
    # Find the day with highest spending
    highest_day = max(daily_spending.items(), key=lambda x: x[1])
    
    # Compare first half of time period with second half to determine trend
    # Uses 10% threshold to determine if change is significant
    trend = "Stable (spending is consistent)"
    if total_days >= 2:
        days_list = sorted(daily_spending.items())
        mid_point = len(days_list) // 2
        
        first_half_avg = sum(v for _, v in days_list[:mid_point]) / max(mid_point, 1)
        second_half_avg = sum(v for _, v in days_list[mid_point:]) / max(len(days_list) - mid_point, 1)
        
        if second_half_avg > first_half_avg * 1.10:
            trend = "Increasing (spending is going up)"
        elif second_half_avg < first_half_avg * 0.90:
            trend = "Decreasing (spending is going down)"
    
    return {
        "trend": trend,
        "average_daily_spending": round(average_daily, 2),
        "highest_spending_day": highest_day[0],
        "highest_spending_amount": highest_day[1]
    }


def get_monthly_comparison(transactions: List[Dict]) -> Dict:
    """Compare spending between consecutive months."""
    monthly_spending = get_time_based_summary(transactions, "monthly")
    
    if len(monthly_spending) < 2:
        return {"message": "Need at least 2 months of data for comparison"}
    
    months = sorted(monthly_spending.keys())
    comparison = {}
    
    for i in range(len(months) - 1):
        current_month = months[i]
        next_month = months[i + 1]
        current_amount = monthly_spending[current_month]
        next_amount = monthly_spending[next_month]
        
        # Calculate percentage change: ((new - old) / old) * 100
        if current_amount > 0:
            percent_change = ((next_amount - current_amount) / current_amount) * 100
        else:
            percent_change = 0
        
        comparison[f"{current_month} to {next_month}"] = {
            "from": current_amount,
            "to": next_amount,
            "percent_change": round(percent_change, 2),
            "direction": "increased" if percent_change > 0 else "decreased" if percent_change < 0 else "no change"
        }
    
    return comparison


def get_category_percentages(transactions: List[Dict]) -> Dict[str, float]:
    """Calculate percentage of total spending for each category."""
    total = get_total_spending(transactions)
    if total == 0:
        return {}
    
    breakdown = get_category_breakdown(transactions)
    percentages = {}
    
    for category, amount in breakdown.items():
        percentage = (amount / total) * 100
        percentages[category] = round(percentage, 2)
    
    return percentages


def get_average_transaction(transactions: List[Dict]) -> float:
    """Calculate average transaction amount."""
    if not transactions:
        return 0.0
    
    total = get_total_spending(transactions)
    average = total / len(transactions)
    return round(average, 2)


def get_highest_transaction(transactions: List[Dict]) -> Optional[Dict]:
    """Find the largest single transaction."""
    if not transactions:
        return None
    
    # Find max by comparing 'amount' field
    highest = max(transactions, key=lambda x: x['amount'])
    return highest


def print_full_statistics(transactions: List[Dict]) -> None:
    """Print complete statistics report to console."""
    if not transactions:
        print("\n" + "="*50)
        print("STATISTICS SUMMARY")
        print("="*50)
        print("\n[INFO] No transactions found.")
        print("       Please add some transactions first using option 1.")
        print("\n" + "="*50)
        return
    
    print("\n" + "="*55)
    print("         PERSONAL BUDGET STATISTICS")
    print("="*55)
    
    # Basic numbers section
    total = get_total_spending(transactions)
    average = get_average_transaction(transactions)
    highest = get_highest_transaction(transactions)
    
    print(f"\n[TOTAL SPENDING]: ${total}")
    print(f"[AVERAGE TRANSACTION]: ${average}")
    if highest:
        print(f"[LARGEST EXPENSE]: ${highest['amount']} ({highest['category']} on {highest['date']})")
    
    # Category breakdown with simple bar chart
    # Each '#' represents 2% of total spending
    print("\n" + "-"*55)
    print("SPENDING BY CATEGORY:")
    print("-"*55)
    
    breakdown = get_category_breakdown(transactions)
    percentages = get_category_percentages(transactions)
    
    for category, amount in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
        percentage = percentages.get(category, 0)
        bar_length = int(percentage / 2)
        bar = "#" * bar_length if bar_length > 0 else "."
        print(f"   {category:12} : ${amount:>8}  ({percentage:>5}%) {bar}")
    
    # Top 3 categories
    print("\n" + "-"*55)
    print("TOP 3 SPENDING CATEGORIES:")
    print("-"*55)
    
    top_categories = get_top_categories(transactions, 3)
    for index, (category, amount) in enumerate(top_categories, 1):
        print(f"   {index}. {category:<12} : ${amount:>8}")
    
    # Monthly breakdown - convert "2024-03" to "March 2024" for display
    print("\n" + "-"*55)
    print("MONTHLY BREAKDOWN:")
    print("-"*55)
    
    monthly_summary = get_time_based_summary(transactions, "monthly")
    for month, amount in sorted(monthly_summary.items()):
        month_name = datetime.strptime(month, "%Y-%m").strftime("%B %Y")
        print(f"   {month_name:15} : ${amount:>8}")
    
    # Spending trends and insights
    print("\n" + "-"*55)
    print("SPENDING INSIGHTS:")
    print("-"*55)
    
    trend_data = get_spending_trend(transactions)
    print(f"   - {trend_data['trend']}")
    print(f"   - Average daily spending: ${trend_data['average_daily_spending']}")
    if trend_data.get('highest_spending_day'):
        print(f"   - Highest spending day: {trend_data['highest_spending_day']} (${trend_data['highest_spending_amount']})")
    
    # Month-to-month comparison
    print("\n" + "-"*55)
    print("MONTH-TO-MONTH COMPARISON:")
    print("-"*55)
    
    comparison = get_monthly_comparison(transactions)
    if "message" in comparison:
        print(f"   [INFO] {comparison['message']}")
    else:
        for period, data in comparison.items():
            if data['direction'] == "increased":
                symbol = "[UP]"
            elif data['direction'] == "decreased":
                symbol = "[DOWN]"
            else:
                symbol = "[SAME]"
            print(f"   {period}:")
            print(f"      ${data['from']} -> ${data['to']} ({symbol} {abs(data['percent_change'])}%)")
    
    print("\n" + "="*55)
