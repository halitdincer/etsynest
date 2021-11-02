from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView,DetailView
from django.views.generic.base import TemplateView

from django.utils import timezone

from .models import Order,OrderItem

class OrderListView(ListView):
    model = Order
    context_object_name = 'listings'
    template_name = "orders/index.html"

    def post(self, request):

        l_data = []

        for order in Order.objects.all():
            if order.created_at:
                l_data.append([order.order_id,
                                timezone.localtime(order.created_at).strftime('%d %B %Y'),
                                order.first_name,
                                order.total_price,
                                order.total_cost
                ])
            else:
                l_data.append([order.order_id,
                                "",
                                order.first_name,
                                order.total_price,
                                order.total_cost
                ])

        context = {}
        context['draw'] = int(request.GET.get('draw',0))+1
        context['recordsTotal'] = len(l_data)
        context['recordsFiltered'] = len(l_data)
        context['data'] = l_data

        return JsonResponse(context, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderDetailView(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = "orders/detail.html"
    slug_field = "order_id"
    slug_url_kwarg = "order_id"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['item_list'] = OrderItem.objects.filter(order=self.object)
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.as_json(), **response_kwargs)
