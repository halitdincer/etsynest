from listings.models import ListingRecord, ListingSnapshot
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

        snapshots = ListingSnapshot.objects.filter(shop=shop).order_by("created_at")

        l_data = []

        for snapshot, next_snapshot in zip(snapshots, snapshots[1:]):

            for record in ListingRecord.objects.filter(snapshot=snapshot):
                next_record = ListingRecord.objects.filter(listing=record.listing,snapshot=next_snapshot).first()
                if next_record and (record.quantity - next_record.quantity) > 0 :
                    l_data.append([ \
                                timezone.localtime(snapshot.created_at).strftime('%d %B %H:%M'), \
                                timezone.localtime(next_snapshot.created_at).strftime('%d %B %H:%M') , \
                                record.listing.listing_id, \
                                record.listing.title[:50] , \
                                record.quantity - next_record.quantity \
                                ])

        context = {}
        context['draw'] = int(request.GET.get('draw',0))+1
        context['recordsTotal'] = len(l_data)
        context['recordsFiltered'] = len(l_data)
        context['data'] = l_data

        return JsonResponse(context, safe=False)
