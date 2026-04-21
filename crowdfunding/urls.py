"""
URL configuration for crowdfunding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects.views import CustomAuthToken, RegisterView, UserViewSet, ProjectViewSet, PledgeViewSet


router = DefaultRouter()

# Users → only index, show, store
router.register(r'users', UserViewSet, basename='users')

# Projects → full control, permissions handled in view
router.register(r'api/projects', ProjectViewSet, basename='projects')

# Pledges → full control
router.register(r'api/pledges', PledgeViewSet, basename='pledges')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    # /user endpoint
    path('user/', UserViewSet.as_view({'get': 'me'})),
    path('api/login/', CustomAuthToken.as_view()),
    path('api/register/', RegisterView.as_view()),
]