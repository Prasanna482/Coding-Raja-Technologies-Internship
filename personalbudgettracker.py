import json
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox
from datetime import datetime

class BudgetTracker:
    def __init__(self):
        self.budget = {
            'income': 0,
            'housing': 0,
            'food': 0,
            'transportation': 0,
            'utilities': 0,
            'entertainment': 0,
            'other': 0
        }
        self.transaction_history = []

    def display_budget(self):
        return "\n".join([f"{category.capitalize()}: ${amount}" for category, amount in self.budget.items()])

    def add_income(self, amount):
        now = datetime.now()
        transaction = {'type': 'income', 'amount': amount, 'date': now.strftime("%Y-%m-%d %H:%M:%S")}
        self.transaction_history.append(transaction)
        self.budget['income'] += amount

    def add_expense(self, category, amount):
        if category.lower() in self.budget:
            now = datetime.now()
            transaction = {'type': 'expense', 'category': category.lower(), 'amount': amount, 'date': now.strftime("%Y-%m-%d %H:%M:%S")}
            self.transaction_history.append(transaction)
            self.budget[category.lower()] -= amount

    def save_data(self, filename='budget_data.json'):
        data = {'budget': self.budget, 'transaction_history': self.transaction_history}
        with open(filename, 'w') as file:
            json.dump(data, file)

    def load_data(self, filename='budget_data.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.budget = data.get('budget', self.budget)
                self.transaction_history = data.get('transaction_history', [])
        except FileNotFoundError:
            pass

class BudgetTrackerGUI:
    def __init__(self, master, tracker):
        self.master = master
        self.tracker = tracker
        master.title("Budget Tracker")

        self.label = Label(master, text="Welcome to the Budget Tracker!")
        self.label.pack()

        self.income_label = Label(master, text="Enter Income:")
        self.income_label.pack()

        self.income_entry = Entry(master)
        self.income_entry.pack()

        self.income_button = Button(master, text="Add Income", command=self.add_income)
        self.income_button.pack()

        self.expense_label = Label(master, text="Enter Expense Category:")
        self.expense_label.pack()

        self.expense_category_entry = Entry(master)
        self.expense_category_entry.pack()

        self.expense_amount_label = Label(master, text="Enter Expense Amount:")
        self.expense_amount_label.pack()

        self.expense_amount_entry = Entry(master)
        self.expense_amount_entry.pack()

        self.expense_button = Button(master, text="Add Expense", command=self.add_expense)
        self.expense_button.pack()

        self.display_button = Button(master, text="Display Budget", command=self.display_budget)
        self.display_button.pack()

        self.save_button = Button(master, text="Save Data", command=self.save_data)
        self.save_button.pack()

        self.load_button = Button(master, text="Load Data", command=self.load_data)
        self.load_button.pack()

        self.exit_button = Button(master, text="Exit", command=master.quit)
        self.exit_button.pack()

    def add_income(self):
        try:
            amount = float(self.income_entry.get())
            self.tracker.add_income(amount)
            messagebox.showinfo("Success", f"Income of ${amount} added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid numerical value.")

    def add_expense(self):
        try:
            category = self.expense_category_entry.get().lower()
            amount = float(self.expense_amount_entry.get())
            self.tracker.add_expense(category, amount)
            messagebox.showinfo("Success", f"Expense of ${amount} in {category.capitalize()} added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid numerical value.")

    def display_budget(self):
        budget_info = self.tracker.display_budget()
        messagebox.showinfo("Current Budget", budget_info)

    def save_data(self):
        self.tracker.save_data()
        messagebox.showinfo("Success", "Data saved successfully.")

    def load_data(self):
        self.tracker.load_data()
        messagebox.showinfo("Success", "Data loaded successfully.")

if __name__ == "__main__":
    tracker = BudgetTracker()

    # Load previous data if available
    tracker.load_data()

    root = Tk()
    gui = BudgetTrackerGUI(root, tracker)
    root.mainloop()