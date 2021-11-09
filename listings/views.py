import datetime,pytz

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView,DetailView,TemplateView
from django.utils import timezone
from etsynest.cron import get_request_Etsy_API_v2

from shops.models import Shop
from listings.models import Listing,ListingRecord, ListingSnapshot
from listings.utils import per_day



class ListingListView(TemplateView):

    template_name = "listings/index.html"

    def post(self, request):

        shop_name = request.POST.get('shop_name','')
        l_data = []
        listings = []

        
        if shop_name != '' and not Shop.objects.filter(name=shop_name).first():
            r_data = get_request_Etsy_API_v2('/shops/' + shop_name + '/listings/active?limit=100',10000)
            for listing in r_data:
                l_data.append([
                            str(listing['listing_id']),
                            datetime.datetime.fromtimestamp(listing['original_creation_tsz'], tz=pytz.UTC).strftime('%d %B %Y'),
                            shop_name,
                            listing['title'][:50] + ' - ' + str(listing['listing_id']),
                            str(listing['quantity']),
                            str(listing['views']),
                            per_day(listing['views'],datetime.datetime.fromtimestamp(listing['original_creation_tsz'], tz=pytz.UTC)),
                            str(listing['num_favorers']),
                            ])

        if shop_name == '':
            listings = Listing.objects.all()
        else :
            listings = Listing.objects.filter(shop=Shop.objects.filter(name=shop_name).first())

        for listing in listings:
            listing_recent_record = ListingRecord.objects.filter(listing=listing).latest('created_at')
            l_data.append([listing.listing_id,
                            timezone.localtime(listing.original_creation_tsz).strftime('%d %B %Y'),
                            listing.shop.name,
                            listing.title[:50] + ' - ' + str(listing.listing_id),
                            listing_recent_record.quantity,
                            listing_recent_record.views,
                            per_day(listing_recent_record.views,timezone.localtime(listing.original_creation_tsz)),
                            listing_recent_record.num_favorers,
                            ])

        context = {}
        context['draw'] = int(request.GET.get('draw',0))+1
        context['recordsTotal'] = len(l_data)
        context['recordsFiltered'] = len(l_data)
        context['data'] = l_data
        return JsonResponse(context, safe=False)

class ListingDetailView(DetailView):
    model = Listing
    context_object_name = 'listing'
    template_name = "listings/detail.html"
    slug_field = "listing_id"
    slug_url_kwarg = "listing_id"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['record_list'] = ListingRecord.objects.filter(listing=self.object)
        return context