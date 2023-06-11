from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path('admin/', admin.site.urls),
    path("auth/", include("purse_auth.urls")),
    path("async/", include("purse_async.urls")),
    path("finance/", include("purse_finance.urls"))
]

if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
