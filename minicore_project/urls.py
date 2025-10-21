"""
URL configuration for minicore_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from gestorventas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('registrar_venta/', views.RegistrarVentaView.as_view(), name='registrar_venta'),
    path('calcular_comisiones/', views.CalcularComisionesView.as_view(), name='calcular_comisiones'),
    path('ventas_exito/', views.VentasExitoView.as_view(), name='ventas_exito'),
]
