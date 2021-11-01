from django.shortcuts import render
from django.views.generic.base import TemplateView

from .cron import update_orders, update_shops

class HomePageView(TemplateView):

    template_name = "etsynest/home.html"

    def get(self, request):
        return render(request, self.template_name, {})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UpdateShopsView(TemplateView):

    template_name = "etsynest/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_shops()
        context['message'] = "Shops Updated."
        return context

class UpdateOrdersView(TemplateView):

    template_name = "etsynest/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_orders()
        context['message'] = "Orders Updated."
        return context