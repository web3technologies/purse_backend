from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models


from phonenumber_field.modelfields import PhoneNumberField

from plaid.exceptions import ApiException as PlaidApiException


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = PhoneNumberField(blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    _liablility_names = ("credit", "loan")

    def __str__(self):
        return self.email
    

    def get_networth(self):
        
        networth_val = 0
        
        items = self.item_set.all()

        for item in items:
            try:
                accounts = item.get_account_data()
            except PlaidApiException:
                accounts = []
            for account in accounts:
                if account.get("type") in self._liablility_names:
                    account["current_balance"] *= -1
                networth_val += account.get("current_balance")

        crypto_accounts = self.cryptoaccount_set.all()

        for crypto_account in crypto_accounts:
            networth_val += crypto_account.value        # do not make request every time because currently too many requests error from api

        return networth_val

