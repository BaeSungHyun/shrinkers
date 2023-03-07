"""shrinkers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from shortener.views import (index, redirect_test, get_user, register, login_view, 
                             logout_view, list_view, url_list, url_create, url_change)
from django.conf import settings
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('redirect/', redirect_test),
    path('register/', register, name='register'),
    path('get_user/<int:user_id>/', get_user),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('list/', list_view, name="list_view"),
    path('urls/', url_list, name='url_list'),
    path('urls/create/', url_create, name="url_create"),
    path('urls/<str:action>/<int:url_id>/', url_change, name="url_change"),
]


# Required for debug_toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns