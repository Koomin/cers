from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

router = DefaultRouter() if settings.DEBUG else SimpleRouter()


app_name = "api"
urlpatterns = router.urls
urlpatterns += [path('stats/', include('cers.stats.urls'))]