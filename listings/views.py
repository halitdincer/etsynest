from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.utils import timezone

from listings.models import Listing,ListingRecord
from listings.utils import per_day

class ListingListView(ListView):
    model = Listing
    context_object_name = 'listings'
    template_name = "listings/index.html"

    def post(self, request):

        l_data = []

        for listing in Listing.objects.all():
            listing_recent_record = ListingRecord.objects.filter(listing=listing).latest('created_at')
            l_data.append([listing.id,
                            timezone.localtime(listing.original_creation_tsz).strftime('%d %B %Y'),
                            listing.shop.name,
                            listing.title[:50] + ' - ' + str(listing.listing_id),
                            listing_recent_record.quantity,
                            listing_recent_record.views,
                            per_day(listing_recent_record.views,listing.original_creation_tsz),
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
    slug_field = "id"
    slug_url_kwarg = "listing_id"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['record_list'] = ListingRecord.objects.filter(listing=self.object)
        return context