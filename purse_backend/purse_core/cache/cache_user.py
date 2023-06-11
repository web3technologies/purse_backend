from django.core.cache import cache
from functools import wraps
from rest_framework.response import Response



def cache_user_view(timeout=60 * 15):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user_id = request.user.id
            cache_key = f"{user_id}:{request.resolver_match.view_name}:{kwargs}"
            cache_key = cache_key.replace(' ', '').replace('\t', '').replace('\n', '')

            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return Response(cached_data)

            response = func(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout)

            return response
        return wrapper
    return decorator


def clear_user_cache():
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user_id = request.user.id
            cache_key = f"{user_id}:{request.resolver_match.view_name}:{kwargs}"
            cache.delete(cache_key)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator