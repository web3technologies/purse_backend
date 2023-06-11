from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.viewsets import ModelViewSet


class CacheModelViewset(ModelViewSet):
    
    cache_period = 60 * 5

    @method_decorator(cache_page(cache_period))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)