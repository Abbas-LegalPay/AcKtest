"""LegalPay_BNPL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Custom router for maintain the versioning of APIs in APIView method.

from django.urls import path, include
from patches import routers

from AccuknoxApp.urls import router as users_routers
from AccuknoxFriendsApp.urls import router as friends_routers

router = routers.DefaultRouter()

router.extend(users_routers)
router.extend(friends_routers)

urlpatterns = [
    path('', include(router.urls)),
]
