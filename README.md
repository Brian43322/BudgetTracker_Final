**Budget Tracker Application (Final Submission)**  
**Author:** Brian
**Course:** Software Development  
**Submission:** Week 5 – Testing & Final Delivery  
**Date:** April 26, 2026  

---

## 📌 **Overview**
The **Budget Tracker Application** is a Python‑based desktop program built with Tkinter. 
It allows users to manage income and expenses, view summaries, filter and sort transactions, and visualize financial data through graphs. 
This project was developed over five weeks, with Week 5 focusing on testing, validation, and final submission packaging.

---

## 🚀 **Features**
### **Core Features**
- Add, edit, and delete transactions  
- Filter by category and type  
- Sort by amount and date  
- Search transactions by title  
- Summary totals (income, expenses, net balance)  
- Graphs (bar chart + pie chart)  
- Multiple UI themes  
- Fullscreen responsive layout  

### **Week 5 Enhancements**
- Persistent data saving using JSON  
- Automatic loading of saved transactions on startup  
- Date validation (MM/DD/YYYY)  
- Added a check for title search if the user inpputed a incorrect/doesn't exist title
- Unit and integration tests using Python `unittest`  
- Final test report  
- Demo video walkthrough  

---

## 🛠 **Technologies Used**
- **Python 3.10+**  
- **Tkinter** (GUI framework)  
- **Matplotlib** (graphs)  
- **JSON** (data persistence)  
- **unittest** (testing framework)

---

## 📂 **Project Structure**
```
Project_BudgetTracker/
│
├── Week5Final.py               # Main application
├── test_budget_tracker.py      # Unit & integration tests
├── transactions.json           # Saved data file
├── README.md                   # Documentation
└── demo_video.mp4              # 3–5 minute walkthrough (included in submission)
```

---

## ▶️ **How to Run the Application**
### **1. Install Dependencies**
Matplotlib is the only external library required:

```
pip install matplotlib
```

Tkinter comes preinstalled with Python.

---

### **2. Run the Application**
From the project folder:

```
python Week5Final.py
```

The application will open in fullscreen and automatically load saved transactions.

---

## 🧪 **How to Run Tests**
All Week 5 tests are located in:

```
test_budget_tracker.py
```

Run them using:

```
python -m unittest test_budget_tracker.py
```

You should see output similar to:

```
.....
OK
```

This indicates all tests passed successfully.

---

## 📊 **Summary of Tests**
The following features were tested:

- Adding transactions  
- Editing transactions  
- Deleting transactions  
- Summary calculations  
- JSON save/load  
- Data integrity  
- Date validation  

All tests passed.

---

## 📝 **Known Issues**
- UI spacing may vary slightly on very small screens  
- Date entry requires manual typing (no date picker widget)  

---

## 🎥 **Demo Video**
A 3–5 minute demonstration video is included in the submission package.  
It covers:

- Adding, editing, deleting transactions  
- Filters, sorting, and search  
- Summary calculations  
- Graphs  
- Theme switching  
- Persistent saving (closing and reopening the app)

---

## 📧 **Author Information**
**Name:** Brian 
**Email:** bagerard@usca.edu  
**Course:** Software Development  
**Instructor:** Mahmoud Omari
