import csv
from datetime import datetime

FILE = "expense_report.csv"
transactions = []
# Load data
def load_data():
    try:
        with open(FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["amount"] = float(row["amount"])
                transactions.append(row)
    except FileNotFoundError:
        pass
# Save data
def save_data():
    with open(FILE, "w", newline="") as f:
        fields = ["date", "type", "category",
                  "amount", "description"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(transactions)
# Add income
def add_income():
    print("--- Add Income ---")
    category = input("Enter Category: ").strip().title()
    
    try:
        amount = float(input("Enter Amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Enter a valid amount.")
        return

    d = input("Date (YYYY-MM-DD): ").strip()
    d = d or datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(d, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    description = input("Enter Description: ").strip()

    transactions.append({
        "date": d,
        "type": "Income",
        "category": category,
        "amount": amount,
        "description": description
    })

    save_data()
    print("Income added successfully.")
# Add expense
def add_expense():
    print("--- Add Expense ---")
    category = input("Category: ").strip().title()

    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Enter a valid amount.")
        return

    d = input("Date (YYYY-MM-DD): ").strip()
    d = d or datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(d, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    description = input("Description: ").strip()

    transactions.append({
        "date": d,
        "type": "Expense",
        "category": category,
        "amount": amount,
        "description": description
    })
    save_data()
    print("Expense added successfully")
# Transaction history
def view_transactions(data=None):
    data = transactions if data is None else data

    print("--- Transaction History ---")

    if not data:
        print("No transactions available")
        return
    for i, t in enumerate(data, 1):
        print(
            f'{i}. {t["date"]} | {t["type"]} | '
            f'{t["category"]} | {float(t["amount"]):.2f} | '
            f'{t["description"]}'
        )
# Search transactions
def search_transactions():
    keyword = input(
        "Search category or description: ").lower()
   
    results = [
        t for t in transactions
        if keyword in t["category"].lower()
        or keyword in t["description"].lower()
    ]

    if not results:
        print("No matching transactions.")
        return

    print("--- Search Results ---")
    view_transactions(results)
# Total summary
def total_summary(data=None):
    data = transactions if data is None else data

    income = sum(
        float(t["amount"]) for t in data
        if t["type"] == "Income"
    )

    expense = sum(
        float(t["amount"]) for t in data
        if t["type"] == "Expense")

    print("--- Total Summary ---")
    print(f"Income : {income:.2f}")
    print(f"Expense: {expense:.2f}")
    print(f"Balance: {income - expense:.2f}")

# Monthly summary
def monthly_summary():
    month = input("Enter month (YYYY-MM): ").strip()

    data = [
        t for t in transactions
        if t["date"].startswith(month)
    ]
    print(f"--- Monthly Summary: {month} ---")
    total_summary(data)
# Category summary
def category_summary():
    summary = {}

    for t in transactions:
        if t["type"] == "Expense":
            category = t["category"]
            summary[category] = (
                summary.get(category, 0)
                + float(t["amount"]))    

    print("--- Category Summary ---")

    if not summary:
        print("No expense data available.")
        return

    for category, amount in summary.items():
        print(f"{category}: {amount:.2f}")
# Export CSV
def export_csv():
    save_data()
    print(f"Report exported successfully: {FILE}")
# Main menu
load_data()

while True:
    print("\n===== PERSONAL EXPENSE TRACKER =====")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Transaction History")
    print("4. Search Transactions")
    print("5. Total Summary")
    print("6. Monthly Summary")
    print("7. Category Summary")
    print("8. Export CSV Report")
    print("9. Exit")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        add_income()
    elif choice == "2":
        add_expense()
    elif choice == "3":
        view_transactions()
    elif choice == "4":
        search_transactions()
    elif choice == "5":
        total_summary()
    elif choice == "6":
        monthly_summary()
    elif choice == "7":
        category_summary()
    elif choice == "8":
        export_csv()
    elif choice == "9":
        print("Thank you for using Expense Tracker")
        break
    else:
        print("Invalid choice. Try again.")
