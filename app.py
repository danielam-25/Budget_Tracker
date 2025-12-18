from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # For flash messages

DATA_FILE = os.path.join('data', 'budgets.json')

def load_budgets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_budgets(budgets):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(budgets, f, indent=4)

@app.route('/')
def index():
    budgets = load_budgets()
    return render_template('index.html', budgets=budgets)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    budgets = load_budgets()
    amount = request.form.get('amount', type=float)
    category_index = request.form.get('category', type=int)

    if amount is None or amount <= 0 or category_index is None or category_index >= len(budgets):
        flash('Invalid expense data.', 'danger')
    else:
        budgets[category_index]['spent'] += amount
        save_budgets(budgets)
        flash('Expense added successfully!', 'success')

    return redirect(url_for('index'))

@app.route('/add_budget')
def add_budget_page():
    return render_template('add_budget.html')

@app.route('/create_budget', methods=['POST'])
def create_budget():
    budgets = load_budgets()
    category = request.form.get('category').strip()
    budget_amount = request.form.get('budget_amount', type=float)

    if not category or budget_amount is None or budget_amount <= 0:
        flash('Invalid budget data.', 'danger')
    elif any(b['category'].lower() == category.lower() for b in budgets):
        flash('Category already exists.', 'danger')
    else:
        budgets.append({'category': category, 'budget': budget_amount, 'spent': 0.0})
        save_budgets(budgets)
        flash('Budget category added successfully!', 'success')

    return redirect(url_for('add_budget_page'))

if __name__ == '__main__':
    app.run(debug=True)