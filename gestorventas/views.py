from django.views.generic import TemplateView, FormView
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import VentaForm
from .services import VentasService
from .models import VendedorModel

class IndexView(TemplateView):
    template_name = 'gestorventas/index.html'


class VentasExitoView(TemplateView):
    template_name = 'gestorventas/ventas_exito.html'


class RegistrarVentaView(FormView):
    template_name = 'gestorventas/registrar_venta.html'
    form_class = VentaForm
    success_url = reverse_lazy('ventas_exito')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendedores, datos_ventas = VentasService.cargar_vendedores_y_ventas()
        context.update({
            'vendedores': vendedores,
            'ventas': datos_ventas,
            'mensaje': kwargs.get('mensaje', ''),
        })
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, mensaje="Formulario inválido. Revisa los datos ingresados."))


class CalcularComisionesView(View):
    template_name = 'gestorventas/calcular_bono.html'

    def get(self, request):
        contexto = {
            'vendedores': VendedorModel.objects.all(),
            'tabla_vendedores': [],
            'mensaje': '',
        }
        return render(request, self.template_name, contexto)

    def post(self, request):
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        vendedor_id = request.POST.get("vendedor") or None

        contexto = {
            'vendedores': VendedorModel.objects.all(),
            'tabla_vendedores': [],
            'mensaje': '',
        }

        try:
            contexto['tabla_vendedores'] = VentasService.calcular_comisiones(vendedor_id, fecha_inicio, fecha_fin)
        except Exception as e:
            contexto['mensaje'] = f"Error al procesar los datos: {e}"

        return render(request, self.template_name, contexto)