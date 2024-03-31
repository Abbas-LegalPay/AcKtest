from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'Friends'
router = routers.DefaultRouter()
router.register(r'friends', FriendsRequestViewSet, basename='friends')

urlpatterns = [
    path('', include(router.urls)),
]
