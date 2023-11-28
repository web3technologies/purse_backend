from rest_framework import routers
from purse_finance.views import *

from django.urls import path

router = routers.SimpleRouter()

router.register(r"budget", BudgetViewset)
router.register(r"item", ItemViewset)
router.register(r"networth", NetWorthViewset)
router.register(r"accounts", PlaidAccountsViewset)
router.register(r'accounts/(?P<account_pk>\d+)/transactions', PlaidTransactionViewset)
router.register(r"account-crypto", CryptoAccountViewSet)



urlpatterns = [
    path("dashboard", DashboardView.as_view()),
    path("get-link-token", LinkTokenView.as_view()),
    path("get-link-token-update", LinkTokenUpdateView.as_view()),
    path("networth-live", NetworthLive.as_view()),
    # Transactions
    path("transactions", TransactionListView.as_view())
]

urlpatterns += router.urls