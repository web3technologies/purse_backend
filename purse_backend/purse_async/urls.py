from rest_framework import routers
from django.urls import path

from purse_async.views import CalculateNetworthView, TaskResultViewset


router = routers.SimpleRouter()

router.register(r"task-results", TaskResultViewset)

urlpatterns = [
    path("calculate-networth", CalculateNetworthView.as_view())
]

urlpatterns += router.urls