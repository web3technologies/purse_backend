# Purse

## Description
The Purse backen is a backend system for managing personal finances. It will connect to Plaid APIS. In order to accurately reflect personal finance data Celery is configured to read data from plaid and populate the account balances. A FrontEnd can be configured to read this data via the rest API's.


## Technology Stack
- **Python**: 3.8
- **Django**: 4.2
- **Celery**: 5.2.7
- **Database**: PostgreSQL
- **Other Dependencies**: djangorestframework, plaid-python

## Installation
Navigate to project directory.
```
python -m venv venv
source ./venv/bin/activate
pip install -e .
```

### Setup
cp exampleenv.txt .env

Need Plaid API accounts and need to api keys for Coinmarketcap, Coinbase, and Alphavantage

# Run Django server
python manage.py runserver

# In a separate terminal, run Celery worker
celery -A purse_async worker --loglevel=info