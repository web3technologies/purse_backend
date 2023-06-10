from .status_vars import (
    ACTIVE,
    LOGIN_REQUIRED,
    INTENAL_ERROR,
)


ITEM_STATUS_CHOICES = (

    (ACTIVE, "Item is active"),
    (LOGIN_REQUIRED, "The item must be re linked with plaid"),
    (INTENAL_ERROR, "The system is not able to handle the error")

)

PLAID_ACCOUNT_STATUS_CHOICES = (

    (ACTIVE, "Item linked to account is active"),
    (LOGIN_REQUIRED, "Item linked to account needs to be re linked")

)


PLAID_ACCOUNT_TYPE_CHOICES = (
    ("INVESTMENT", "INVESTMENT"),
    ("ASSET", "ASSET"),
    ("DEPOSITORY", "DEPOSITORY"),
    ("LOAN", "LOAN"),
    ("CREDIT", "CREDIT")
)

ACCOUNT_TYPE_CHOICES = (
    ("CRYPTO", "CRYPTO"),
    ("PLAID", "PLAID") 
)


MESSAGE_CHOICE_TYPES = (
    ("SMS", "SMS"),
    ("Email", "Email") 
)