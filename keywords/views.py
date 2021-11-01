from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import TemplateView

from etsynest.cron import get_request_Etsy_API_v2


class KeywordListView(TemplateView):

    template_name = "keywords/index.html"

    def post(self, request):

        keyword_list = {}
        total_result = 2
        
        # GET keywords
        keywords = request.POST.get('keywords','halloween')
        detailsearch = request.POST.get('detailsearch','false')

        if detailsearch == 'true':
            total_result = 5

        # API call Etsy to receive data
        r_data = get_request_Etsy_API_v2('/listings/active?limit=100&sort_on=score&keywords=' + keywords, total_result) ;

        for listing in r_data:
            if 'tags' in listing.keys():
                for tag in listing['tags']:
                    if tag.lower() in keyword_list.keys():
                        keyword_list[tag.lower()]['count'] = keyword_list[tag.lower()]['count'] + 1
                        keyword_list[tag.lower()]['popularity'] = keyword_list[tag.lower()]['popularity'] + listing['views']
                    else:
                        keyword_list[tag.lower()] = {
                            'count' : 1,
                            'popularity' : listing['views']
                        }


        l_data = []
        for keyword in keyword_list.keys():
            l_data.append([
                keyword,
                keyword_list[keyword]['count'],
                keyword_list[keyword]['popularity'],
                "{:.2f}".format(keyword_list[keyword]['popularity']/keyword_list[keyword]['count'])])

        context = {}
        context['draw'] = int(request.GET.get('draw',0))+1
        context['recordsTotal'] = len(l_data)
        context['recordsFiltered'] = len(l_data)
        context['data'] = l_data

        return JsonResponse(context, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
