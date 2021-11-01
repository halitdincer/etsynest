from listings.models import ListingRecord
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.utils import timezone

from shops.models import Shop

from listings.models import Listing,ListingRecord

class ShopListView(ListView):
    model = Shop
    context_object_name = 'shops'
    template_name = "shops/index.html"

    def post(self, request):

        l_data = []

        for shop in Shop.objects.all():
            l_data.append([shop.name,0,0,0,0])

        context = {}
        context['draw'] = int(request.GET.get('draw',0))+1
        context['recordsTotal'] = len(l_data)
        context['recordsFiltered'] = len(l_data)
        context['data'] = l_data
        return JsonResponse(context, safe=False)

class ShopDetailView(DetailView):
    model = Shop
    context_object_name = "shop"
    template_name = "shops/detail.html"
    slug_field = "name"
    slug_url_kwarg = "shop_name"

    def post(self, request, shop_name):

        shop = self.get_object()
        print("Shop Name:" + shop.name)

        l_data = []

        for listing in Listing.objects.filter(shop=shop):
            for lr in ListingRecord.objects.filter(listing=listing):
                l_data.append([listing.id,listing.title[:50] + ' - ' + str(listing.listing_id),timezone.localtime(lr.created_at).strftime('%d % %H:%M'),lr.quantity,lr.num_favorers,lr.price])

        context = {}
        context['draw'] = int(request.GET.get('draw',0))+1
        context['recordsTotal'] = len(l_data)
        context['recordsFiltered'] = len(l_data)
        context['data'] = l_data

        return JsonResponse(context, safe=False)
