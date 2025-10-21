from django.contrib import admin
from .models import VendedorModel, VentasModel, ReglasModel

@admin.register(VendedorModel)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('vendedorId', 'nombreVendedor', 'apellidoVendedor')
    search_fields = ('nombreVendedor', 'apellidoVendedor')

@admin.register(VentasModel)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('ventaId', 'vendedorId', 'cantidadVenta', 'fechaVenta')
    list_filter = ('fechaVenta', 'vendedorId')
    search_fields = ('vendedorId__nombreVendedor', 'vendedorId__apellidoVendedor')

@admin.register(ReglasModel)
class ReglasAdmin(admin.ModelAdmin):
    list_display = ('reglaId', 'metaVenta', 'cantidadComision')
    ordering = ('-metaVenta',)