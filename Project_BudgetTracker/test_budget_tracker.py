import unittest
import json
import os
from Week5Final import transactions, add_or_update_transaction, delete_transaction, update_summary

class TestBudgetTracker(unittest.TestCase):

    def setUp(self):
        # Reset transactions before each test
        transactions.clear()

    def test_add_transaction(self):
        transactions.append({
            "title": "Paycheck",
            "amount": 1000,
            "date": "04/20/2026",
            "category": "Income",
            "type": "Income"
        })
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["amount"], 1000)

    def test_edit_transaction(self):
        transactions.append({
            "title": "Groceries",
            "amount": 50,
            "date": "04/21/2026",
            "category": "Food",
            "type": "Expense"
        })
        transactions[0]["amount"] = 75
        self.assertEqual(transactions[0]["amount"], 75)

    def test_delete_transaction(self):
        transactions.append({"title": "Rent", "amount": 900, "date": "04/01/2026", "category": "Bills", "type": "Expense"})
        transactions.pop(0)
        self.assertEqual(len(transactions), 0)

    def test_summary_calculations(self):
        transactions.append({"title": "Paycheck", "amount": 1000, "date": "04/20/2026", "category": "Income", "type": "Income"})
        transactions.append({"title": "Groceries", "amount": 200, "date": "04/21/2026", "category": "Food", "type": "Expense"})

        total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")
        net = total_income - total_expense

        self.assertEqual(total_income, 1000)
        self.assertEqual(total_expense, 200)
        self.assertEqual(net, 800)

    def test_json_save_load(self):
        test_data = [
            {"title": "Test", "amount": 123, "date": "04/22/2026", "category": "Other", "type": "Expense"}
        ]

        with open("test_data.json", "w") as f:
            json.dump(test_data, f)

        with open("test_data.json", "r") as f:
            loaded = json.load(f)

        self.assertEqual(loaded[0]["amount"], 123)

        os.remove("test_data.json")

if __name__ == "__main__":
    unittest.main()
