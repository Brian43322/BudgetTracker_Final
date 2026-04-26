import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# ---------------- DATA ----------------

DATA_FILE = "transactions.json"
transactions = []
selected_index = None
current_sort_column = None
current_sort_reverse = False

# ---------------- SAVE & LOAD ----------------

def save_data():
    """Save all transactions to JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(transactions, f, indent=4)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save data:\n{e}")

def load_data():
    """Load transactions from JSON file if it exists."""
    global transactions
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                transactions = json.load(f)
        except:
            transactions = []
    else:
        transactions = []

# ---------------- THEMES ----------------

DEFAULT_THEME = {
    "bg": "#F5F5F5",
    "card": "#FFFFFF",
    "text": "#000000",
    "primary": "#4A90E2",
    "primary_dark": "#357ABD",
    "danger": "#D9534F",
    "danger_dark": "#C9302C",
    "header": "#4A90E2"
}

EXECUTIVE_THEME = {
    "bg": "#1A1A1A",
    "card": "#2A2A2A",
    "text": "#FFFFFF",
    "primary": "#C1121F",
    "primary_dark": "#8B0D18",
    "danger": "#D4AF37",
    "danger_dark": "#A8892C",
    "header": "#000000"
}

STUDENT_THEME = {
    "bg": "#E8F4FF",
    "card": "#FFFFFF",
    "text": "#1A3A5F",
    "primary": "#4A90E2",
    "primary_dark": "#357ABD",
    "danger": "#F5C518",
    "danger_dark": "#C49B12",
    "header": "#4A90E2"
}

MINIMALIST_THEME = {
    "bg": "#F2F2F2",
    "card": "#FFFFFF",
    "text": "#333333",
    "primary": "#A3A3A3",
    "primary_dark": "#7A7A7A",
    "danger": "#D9534F",
    "danger_dark": "#C9302C",
    "header": "#E5E5E5"
}

GAMER_THEME = {
    "bg": "#0D0D0D",
    "card": "#1A1A1A",
    "text": "#E0E0E0",
    "primary": "#00E5FF",
    "primary_dark": "#00B3CC",
    "danger": "#B300FF",
    "danger_dark": "#7A00B3",
    "header": "#121212"
}

NATURE_THEME = {
    "bg": "#E9F5EC",
    "card": "#FFFFFF",
    "text": "#2F4F2F",
    "primary": "#6DAA6C",
    "primary_dark": "#4F7F50",
    "danger": "#A0522D",
    "danger_dark": "#7A3D22",
    "header": "#6DAA6C"
}

LUXURY_THEME = {
    "bg": "#000000",
    "card": "#1A1A1A",
    "text": "#FFFFFF",
    "primary": "#D4AF37",
    "primary_dark": "#A8892C",
    "danger": "#FF4C4C",
    "danger_dark": "#CC3D3D",
    "header": "#000000"
}

PARENT_THEME = {
    "bg": "#F7F2E8",
    "card": "#FFFFFF",
    "text": "#2C3E50",
    "primary": "#6FA8DC",
    "primary_dark": "#3C6E91",
    "danger": "#E57373",
    "danger_dark": "#C94F4F",
    "header": "#6FA8DC"
}

def apply_theme(theme):
    root.configure(bg=theme["bg"])
    header.configure(bg=theme["header"])
    header_label.configure(bg=theme["header"], fg="white")

    theme_bar.configure(bg=theme["bg"])
    for widget in theme_bar.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=theme["bg"], fg=theme["text"])

    for frame in [form_frame, filter_frame, summary_frame, table_frame]:
        frame.configure(bg=theme["card"])
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=theme["card"], fg=theme["text"])

    add_button.configure(bg=theme["primary"], fg="white")
    delete_button.configure(bg=theme["danger"], fg="white")
    reset_button.configure(bg=theme["primary"], fg="white")
    graph_button.configure(bg=theme["primary"], fg="white")

# ---------------- CRUD ----------------
def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%m/%d/%Y")
        return True
    except ValueError:
        return False

def add_or_update_transaction():
    global selected_index

    title = title_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()
    category = category_var.get()
    ttype = type_var.get()

    # REQUIRED FIELD CHECK
    if not title or not amount or not date:
        messagebox.showerror("Error", "All fields must be filled.")
        return

    # DATE VALIDATION (INSIDE FUNCTION)
    if not validate_date(date):
        messagebox.showerror("Error", "Invalid date format. Use MM/DD/YYYY.")
        return

    # AMOUNT VALIDATION
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be numeric.")
        return

    # BUILD TRANSACTION
    transaction = {
        "title": title,
        "amount": amount,
        "date": date,
        "category": category,
        "type": ttype
    }

    # UPDATE OR ADD
    if selected_index is not None:
        transactions[selected_index] = transaction
        selected_index = None
        add_button.config(text="Add Transaction")
    else:
        transactions.append(transaction)

    save_data()
    update_table()
    update_summary()
    clear_form()


def clear_form():
    title_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    category_var.set("")
    type_var.set("Income")

def update_table(filtered_list=None):
    for row in table.get_children():
        table.delete(row)

    data = filtered_list if filtered_list else transactions

    for t in data:
        table.insert("", tk.END, values=(
            t["date"], t["title"], t["category"], t["type"], f"{t['amount']:.2f}"
        ))

def on_row_select(event):
    global selected_index

    selected = table.focus()
    if not selected:
        return

    values = table.item(selected, "values")
    selected_index = table.index(selected)

    date_entry.delete(0, tk.END)
    date_entry.insert(0, values[0])

    title_entry.delete(0, tk.END)
    title_entry.insert(0, values[1])

    category_var.set(values[2])
    type_var.set(values[3])

    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, values[4])

    add_button.config(text="Update Transaction")

def delete_transaction():
    global selected_index

    selected = table.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a transaction to delete.")
        return

    if not messagebox.askyesno("Confirm", "Delete this transaction?"):
        return

    index = table.index(selected)
    transactions.pop(index)

    save_data()
    update_table()
    update_summary()
    clear_form()
    add_button.config(text="Add Transaction")
    selected_index = None

# ---------------- FILTERING ----------------

def apply_filters():
    filtered = transactions.copy()

    # SEARCH TITLE
    search_text = search_var.get().lower()
    if search_text:
        filtered = [t for t in filtered if search_text in t["title"].lower()]

        if len(filtered) == 0:
            update_table([])
            messagebox.showinfo("No Results", f"No transactions found with title containing: '{search_text}'")
            return

    # CATEGORY FILTER
    cat = filter_category_var.get()
    if cat != "All":
        filtered = [t for t in filtered if t["category"] == cat]

        if len(filtered) == 0:
            update_table([])
            messagebox.showinfo("No Results", f"No transactions found in category: '{cat}'")
            return

    # TYPE FILTER
    ttype = filter_type_var.get()
    if ttype != "All":
        filtered = [t for t in filtered if t["type"] == ttype]

        if len(filtered) == 0:
            update_table([])
            messagebox.showinfo("No Results", f"No transactions found for type: '{ttype}'")
            return

    # SORTING
    sort_option = sort_var.get()
    if sort_option == "Amount: Smallest → Largest":
        filtered.sort(key=lambda x: x["amount"])
    elif sort_option == "Amount: Largest → Smallest":
        filtered.sort(key=lambda x: x["amount"], reverse=True)
    elif sort_option == "Date: Oldest → Newest":
        filtered.sort(key=lambda x: x["date"])
    elif sort_option == "Date: Newest → Oldest":
        filtered.sort(key=lambda x: x["date"], reverse=True)

    update_table(filtered)


def reset_filters():
    search_var.set("")
    filter_category_var.set("All")
    filter_type_var.set("All")
    sort_var.set("None")
    update_table()

# ---------------- SUMMARY ----------------

def update_summary():
    total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    net = total_income - total_expense

    income_label.config(text=f"Total Income: ${total_income:.2f}")
    expense_label.config(text=f"Total Expenses: ${total_expense:.2f}")
    net_label.config(text=f"Net Balance: ${net:.2f}")

# ---------------- GRAPHS ----------------

def show_graphs():
    if not transactions:
        messagebox.showinfo("No Data", "No transactions to graph.")
        return

    graph_window = tk.Toplevel(root)
    graph_window.title("Financial Graphs")
    graph_window.geometry("900x600")

    income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")

    fig, axs = plt.subplots(1, 2, figsize=(10, 4))

    axs[0].bar(["Income", "Expenses"], [income, expense], color=["green", "red"])
    axs[0].set_title("Income vs Expenses")

    categories = {}
    for t in transactions:
        categories[t["category"]] = categories.get(t["category"], 0) + t["amount"]

    axs[1].pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%")
    axs[1].set_title("Category Breakdown")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# ---------------- UI SETUP ----------------

root = tk.Tk()
root.title("Budget Tracker - Week 5 Final")
root.state("zoomed")

# FULLSCREEN EXPANSION
for col in range(4):
    root.columnconfigure(col, weight=1)
for row in range(6):
    root.rowconfigure(row, weight=1)

# Header
header = tk.Frame(root, height=60)
header.grid(row=0, column=0, columnspan=4, sticky="nsew")
header_label = tk.Label(header, text="Budget Tracker", font=("Segoe UI", 20, "bold"))
header_label.pack(pady=10)

# Theme Bar
theme_bar = tk.Frame(root)
theme_bar.grid(row=1, column=0, columnspan=4, sticky="nsew")
theme_bar.columnconfigure(0, weight=1)
theme_bar.columnconfigure(1, weight=1)
theme_bar.columnconfigure(2, weight=1)
theme_bar.columnconfigure(3, weight=1)

theme_label = tk.Label(theme_bar, text="Theme:")
theme_label.pack(side="left", padx=10)

theme_var = tk.StringVar(value="Default")
theme_dropdown = ttk.Combobox(theme_bar, textvariable=theme_var, width=18, state="readonly")
theme_dropdown["values"] = ["Default","Executive","Student","Minimalist","Gamer","Nature","Luxury","Parent"]
theme_dropdown.pack(side="left", padx=5)

theme_dropdown.bind("<<ComboboxSelected>>", lambda e: apply_theme(eval(theme_var.get().upper() + "_THEME")))

# Search
search_var = tk.StringVar()
tk.Label(theme_bar, text="Search Title:").pack(side="left", padx=10)
search_entry = tk.Entry(theme_bar, textvariable=search_var, width=25)
search_entry.pack(side="left", padx=5)
tk.Button(theme_bar, text="Apply Search", command=apply_filters).pack(side="left", padx=10)

# Form Frame
form_frame = tk.Frame(root, bd=1, relief="solid")
form_frame.grid(row=2, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")
form_frame.columnconfigure(1, weight=1)

ENTRY_WIDTH = 22

tk.Label(form_frame, text="Title").grid(row=0, column=0, padx=10, pady=10, sticky="e")
title_entry = tk.Entry(form_frame, width=ENTRY_WIDTH)
title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

tk.Label(form_frame, text="Amount").grid(row=1, column=0, padx=10, pady=10, sticky="e")
amount_entry = tk.Entry(form_frame, width=ENTRY_WIDTH)
amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

tk.Label(form_frame, text="Date (MM/DD/YYYY)").grid(row=2, column=0, padx=10, pady=10, sticky="e")
date_entry = tk.Entry(form_frame, width=ENTRY_WIDTH)
date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

tk.Label(form_frame, text="Category").grid(row=3, column=0, padx=10, pady=10, sticky="e")
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(form_frame, textvariable=category_var, width=ENTRY_WIDTH - 2, state="readonly")
category_dropdown["values"] = ["Income","Food","Bills","Entertainment","Other"]
category_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Type Row
tk.Label(form_frame, text="Type").grid(row=4, column=0, padx=10, pady=10, sticky="e")
type_var = tk.StringVar(value="Income")

type_frame = tk.Frame(form_frame, bg=form_frame["bg"])
type_frame.grid(row=4, column=1, padx=10, pady=10, sticky="w")

ttk.Radiobutton(type_frame, text="Income", variable=type_var, value="Income").pack(side="left", padx=5)
ttk.Radiobutton(type_frame, text="Expense", variable=type_var, value="Expense").pack(side="left", padx=5)

# Buttons Row
button_frame = tk.Frame(form_frame, bg=form_frame["bg"])
button_frame.grid(row=5, column=1, columnspan=2, padx=10, pady=20, sticky="w")

add_button = tk.Button(button_frame, text="Add Transaction", width=18, command=add_or_update_transaction)
add_button.pack(side="left", padx=5)

delete_button = tk.Button(button_frame, text="Delete Transaction", width=18, command=delete_transaction)
delete_button.pack(side="left", padx=5)

# Filter Frame
filter_frame = tk.Frame(root, bd=1, relief="solid")
filter_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

tk.Label(filter_frame, text="Filter by Category:").grid(row=0, column=0, padx=10, pady=10)
filter_category_var = tk.StringVar(value="All")
filter_category = ttk.Combobox(filter_frame, textvariable=filter_category_var, width=15, state="readonly")
filter_category["values"] = ["All","Income","Food","Bills","Entertainment","Other"]
filter_category.grid(row=0, column=1, padx=10, pady=10)

tk.Label(filter_frame, text="Filter by Type:").grid(row=0, column=2, padx=10, pady=10)
filter_type_var = tk.StringVar(value="All")
filter_type = ttk.Combobox(filter_frame, textvariable=filter_type_var, width=15, state="readonly")
filter_type["values"] = ["All","Income","Expense"]
filter_type.grid(row=0, column=3, padx=10, pady=10)

tk.Label(filter_frame, text="Sort by:").grid(row=0, column=4, padx=10, pady=10)
sort_var = tk.StringVar(value="None")
sort_dropdown = ttk.Combobox(filter_frame, textvariable=sort_var, width=28, state="readonly")
sort_dropdown["values"] = [
    "None",
    "Amount: Smallest → Largest",
    "Amount: Largest → Smallest",
    "Date: Oldest → Newest",
    "Date: Newest → Oldest"
]
sort_dropdown.grid(row=0, column=5, padx=10, pady=10)

apply_filter_button = tk.Button(filter_frame, text="Apply Filters", command=apply_filters)
apply_filter_button.grid(row=0, column=6, padx=10, pady=10)

reset_button = tk.Button(filter_frame, text="Reset Filters", command=reset_filters)
reset_button.grid(row=0, column=7, padx=10, pady=10)

# Summary Frame
summary_frame = tk.Frame(root, bd=1, relief="solid")
summary_frame.grid(row=4, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

income_label = tk.Label(summary_frame, text="Total Income: $0.00", font=("Segoe UI", 12, "bold"))
income_label.grid(row=0, column=0, padx=20, pady=10)

expense_label = tk.Label(summary_frame, text="Total Expenses: $0.00", font=("Segoe UI", 12, "bold"))
expense_label.grid(row=0, column=1, padx=20, pady=10)

net_label = tk.Label(summary_frame, text="Net Balance: $0.00", font=("Segoe UI", 12, "bold"))
net_label.grid(row=0, column=2, padx=20, pady=10)

graph_button = tk.Button(summary_frame, text="Show Graphs", command=show_graphs)
graph_button.grid(row=0, column=3, padx=20, pady=10)

# ---------------- TABLE FRAME ----------------

table_frame = tk.Frame(root, bd=1, relief="solid")
table_frame.grid(row=5, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")
table_frame.columnconfigure(0, weight=1)

columns = ("date", "title", "category", "type", "amount")
table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col.capitalize())
    table.column(col, anchor="center", width=150)

table.pack(fill="both", expand=True, padx=10, pady=10)
table.bind("<<TreeviewSelect>>", on_row_select)

# ---------------- LOAD DATA + INITIALIZE ----------------

load_data()
update_table()
update_summary()

# Apply default theme
apply_theme(DEFAULT_THEME)

root.mainloop()
