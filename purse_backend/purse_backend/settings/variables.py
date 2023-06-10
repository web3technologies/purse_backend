from decouple import config

from purse_core.settings import *


###PLAID
PLAID_CLIENT_ID = config("PLAID_CLIENT_ID")
PLAID_SECRET = config("PLAID_SECRET")
PLAID_REDIRECT_URI = config("PLAID_REDIRECT_URI")
PLAID_ENV = config("PLAID_ENV")


###CAPITAL ONE
CAPITAL_ONE_HOSTNAME=config("CAPITAL_ONE_HOSTNAME")
CAPITAL_ONE_CLIENT_ID=config("CAPITAL_ONE_CLIENT_ID")
CAPITAL_ONE_SECRET=config("CAPITAL_ONE_SECRET")

###COINBASE
COINBASE_API_KEY=config("COINBASE_API_KEY")
COINBASE_SECRET_KEY=config("COINBASE_SECRET_KEY")

###COINMARKETCAP
COINMARKETCAP_URL = config("COINMARKETCAP_URL")
COINMARKETCAP_API_KEY = config("COINMARKETCAP_API_KEY")

###AlphaVantage
ALPHAVANTAGE_URL = config("ALPHAVANTAGE_URL")
ALPHAVANTAGE_API_KEY = config("ALPHAVANTAGE_API_KEY")

# GMAIL_USER = config("GMAIL_USER")
# GMAIL_APP_PASSWORD = config("GMAIL_APP_PASSWORD")

TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")

###SCHEDULE
CALCULATE_ALL_USER_NETWORTH_AND_NOTIFY_TASK_INTERVAL = config("CALCULATE_ALL_USER_NETWORTH_AND_NOTIFY_TASK_INTERVAL")
RETRIEVE_PLAID_ACCOUNT_DATA_FOR_ALL_USERS_TASK_INTERVAL = config("RETRIEVE_PLAID_ACCOUNT_DATA_FOR_ALL_USERS_TASK_INTERVAL")
RETRIEVE_CRYPTO_ACCOUNT_VALUE_FOR_ALL_USERS_TASK_INTERVAL = config("RETRIEVE_CRYPTO_ACCOUNT_VALUE_FOR_ALL_USERS_TASK_INTERVAL")

#TASK ENABLE
CALCULATE_ALL_USER_NETWORTH_AND_NOTIFY_TASK_ENABLE = config("CALCULATE_ALL_USER_NETWORTH_AND_NOTIFY_TASK_ENABLE")
RETRIEVE_PLAID_ACCOUNT_DATA_FOR_ALL_USERS_TASK_ENABLE = config("RETRIEVE_PLAID_ACCOUNT_DATA_FOR_ALL_USERS_TASK_ENABLE")
RETRIEVE_CRYPTO_ACCOUNT_VALUE_FOR_ALL_USERS_TASK_ENABLE = config("RETRIEVE_CRYPTO_ACCOUNT_VALUE_FOR_ALL_USERS_TASK_ENABLE")