
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.utils.decorators import method_decorator

from purse_core.cache.cache_user import cache_user_view, clear_user_cache
from purse_finance.models import NetWorth
from purse_finance.serializers.networth import NetWorthSerializer


class NetWorthViewset(ModelViewSet):
    queryset = NetWorth.objects.all()
    serializer_class = NetWorthSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by("date")

    def list(self, request, *args, **kwargs):
        stored_networths = [
                {"networth": networth.networth, "date": networth.date} 
                for networth 
                in self.get_queryset().order_by("date")
            ]
        return Response(data=stored_networths, status=HTTP_200_OK)


class NetworthLive(APIView):

    @method_decorator(cache_user_view())
    def get(self, request, *args, **kwargs):
        current_networth = request.user.get_networth()
        res = {
                "networth": current_networth,
                "date": timezone.now()
            }
        return Response(data=res, status=status.HTTP_200_OK)

    @method_decorator(clear_user_cache())
    def post(self, request):
        return Response(data={"detail": "cache cleared"}, status=status.HTTP_201_CREATED)