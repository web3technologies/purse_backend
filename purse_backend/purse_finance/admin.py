from django.contrib import admin

from purse_finance.models import Budget, Item, NetWorth, PlaidAccount, CryptoAccount


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    ...

@admin.register(NetWorth)
class ItemAdmin(admin.ModelAdmin):
    ...

@admin.register(PlaidAccount)
class AccountAdmin(admin.ModelAdmin):
    ...

@admin.register(CryptoAccount)
class AccountAdmin(admin.ModelAdmin):
    ...

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    ...