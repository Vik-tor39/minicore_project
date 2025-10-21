from decimal import Decimal, InvalidOperation, getcontext
from datetime import datetime, date
from django.db.models import Sum
from .models import VentasModel, ReglasModel, VendedorModel

getcontext().prec = 28

class VentasService:
    @staticmethod
    def _parse_date(value):
        if value is None or value == '':
            return None
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except Exception:
            raise ValueError(f"Fecha inválida: {value}. Use formato YYYY-MM-DD.")

    @staticmethod
    def obtener_ventas_por_vendedor(vendedor_id, fecha_inicio, fecha_fin):
        fi = VentasService._parse_date(fecha_inicio)
        ff = VentasService._parse_date(fecha_fin)

        qs = VentasModel.objects.all()
        if vendedor_id:
            qs = qs.filter(vendedorId_id=vendedor_id)

        if fi and ff:
            if fi > ff:
                raise ValueError("La fecha de inicio no puede ser posterior a la fecha fin.")
            qs = qs.filter(fechaVenta__range=(fi, ff))
        elif fi:
            qs = qs.filter(fechaVenta__gte=fi)
        elif ff:
            qs = qs.filter(fechaVenta__lte=ff)

        agg = qs.aggregate(total=Sum('cantidadVenta'))
        total = agg.get('total') or Decimal('0.00')
        try:
            total = Decimal(total)
        except (InvalidOperation, TypeError):
            total = Decimal('0.00')
        return total

    @staticmethod
    def obtener_regla_para_ventas(ventas_totales):
        if ventas_totales is None:
            ventas_totales = Decimal('0.00')
        return ReglasModel.objects.filter(metaVenta__lte=ventas_totales).order_by('-metaVenta').first()

    @staticmethod
    def calcular_comisiones(vendedor_id, fecha_inicio, fecha_fin):
        fi = fecha_inicio
        ff = fecha_fin

        if vendedor_id:
            ventas_totales = VentasService.obtener_ventas_por_vendedor(vendedor_id, fi, ff)
            regla = VentasService.obtener_regla_para_ventas(ventas_totales)
            if regla:
                bono = (ventas_totales * (regla.cantidadComision / Decimal('100'))).quantize(Decimal('0.01'))
            else:
                bono = Decimal('0.00')

            vendedor_obj = None
            try:
                vendedor_obj = VendedorModel.objects.get(pk=vendedor_id)
                nombre = f"{vendedor_obj.nombreVendedor} {vendedor_obj.apellidoVendedor}"
            except VendedorModel.DoesNotExist:
                nombre = f"Vendedor {vendedor_id}"

            return [{
                'nombre': nombre,
                'ventas_totales': ventas_totales,
                'meta_venta': regla.metaVenta if regla else Decimal('0.00'),
                'comision': regla.cantidadComision if regla else Decimal('0.00'),
                'bono': bono,
            }]
        else:
            vendedores = VendedorModel.objects.all()
            tabla = []
            for v in vendedores:
                ventas_totales = VentasService.obtener_ventas_por_vendedor(v.vendedorId, fi, ff)
                regla = VentasService.obtener_regla_para_ventas(ventas_totales)
                bono = (ventas_totales * (regla.cantidadComision / Decimal('100'))).quantize(Decimal('0.01')) if regla else Decimal('0.00')
                tabla.append({
                    'nombre': f"{v.nombreVendedor} {v.apellidoVendedor}",
                    'ventas_totales': ventas_totales,
                    'meta_venta': regla.metaVenta if regla else Decimal('0.00'),
                    'comision': regla.cantidadComision if regla else Decimal('0.00'),
                    'bono': bono,
                })
            return tabla

    @staticmethod
    def cargar_vendedores_y_ventas(limit=100):
        vendedores = VendedorModel.objects.all()
        ventas = VentasModel.objects.select_related('vendedorId').order_by('-fechaVenta')[:limit]
        datos_ventas = []
        for venta in ventas:
            datos_ventas.append({
                'vendedor_nombre': f"{venta.vendedorId.nombreVendedor} {venta.vendedorId.apellidoVendedor}",
                'cantidadVenta': venta.cantidadVenta,
                'fechaVenta': venta.fechaVenta,
            })
        return vendedores, datos_ventas
