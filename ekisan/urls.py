"""ekisan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('buying/', views.buying, name='buying'),
    path('selling/', views.selling, name='selling'),
    path('program/', views.program, name='program'),
    path('contact/', views.contact, name='contact'),
    path('farmsignUp/', views.farmsignUp, name='farmsignUp'),
    path('fsignin/', views.fsignin, name='fsignin'),
    path('additem/', views.additem, name='additem'),
    path('edititem/', views.edititem, name='edititem'),
    path('about/', views.about, name='about'),
    path('Clogin/', views.Clogin, name='Clogin'),
    path('Csignup/', views.Csignup, name='Csignup'),
    path('mainpro/',views.mainpro,name='mainpro'),
    path('addtocart/',views.addtocart,name='addtocart'),
    path('displaycart/',views.displaycart,name='displaycart'),
    path('consumerlogin/', views.consumerlogin, name='consumerlogin'),
    path('removefromcart/', views.removefromcart, name='removefromcart'),
    path('razor/',views.razor,name='razor'),
    path('success/',views.success,name='success'),
    path('signup/',views.signup,name='signup'),

]
