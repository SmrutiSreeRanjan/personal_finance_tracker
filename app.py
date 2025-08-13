from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'transactions.csv'

def read_transactions():
    transactions = []
    try:
        with open(DATA_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = float(row['amount'])
                transactions.append(row)
    except FileNotFoundError:
        pass
    return transactions

def write_transaction(transaction):
    file_exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, mode='a', newline='') as file:
        fieldnames = ['date', 'category', 'type', 'amount', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(transaction)

def get_balance(transactions):
    income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
    expense = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
    return income - expense

@app.route('/')
def index():
    transactions = read_transactions()
    balance = get_balance(transactions)
    return render_template('index.html', transactions=transactions, balance=balance)

@app.route('/add', methods=['POST'])
def add_transaction():
    transaction = {
        'date': request.form['date'],
        'category': request.form['category'],
        'type': request.form['type'],
        'amount': float(request.form['amount']),
        'description': request.form['description']
    }
    write_transaction(transaction)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
