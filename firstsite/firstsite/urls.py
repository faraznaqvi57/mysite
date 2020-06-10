"""firstsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_page,name="home_page"),
    path('aboutus/',views.aboutus,name="aboutus"),
    path('match_details/<int:id>/',views.match_details,name="match_details"),
    path('match_calender/',views.match_calender,name='match_calender'),
    path('search/<int:id>/',views.search,name='search'),
    path('custom_team/<int:id>/<str:match_type>/',views.custom_team,name="custom_team"),
    path('custom_match/',views.custom_match,name="custom_match"),
    path('prediction/<int:id>/',views.prediction,name="prediction")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
