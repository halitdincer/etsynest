import requests,json,os
import datetime,pytz

from requests_oauthlib import OAuth1,OAuth1Session

from etsy_config import ETSY_API_KEY, ETSY_BASE_URL,ETSY_CLIENT_SECRET, ETSY_SHOP_ID
from etsy_config import ETSY_RESOURCE_OWNER_KEY,ETSY_RESOURCE_OWNER_SECRET

from shops.models import Shop
from orders.models import Order

from listings.models import Listing,ListingRecord

from printify_config import PRINTIFY_SHOP_ID,PRINTIFY_URL, PRINTIFY_API_KEY

def get_request_Printify_API(url_ext):
    """
        Getting orders data from Printify API and saving in data.txt at main folder
    """

    i = 1
    orders = []

    B_HEADER = {"Authorization": "Bearer " + PRINTIFY_API_KEY }

    url = PRINTIFY_URL + url_ext

    resp = requests.get(url,headers=B_HEADER)

    while 'json' in resp.headers.get('Content-Type') and 'data' in resp.json().keys() and i<10000:

        if resp.status_code != 200: 
            print("Something is wrong!!!")

        orders.extend(resp.json()['data'])
        print("Page " + str(i) + " loaded")
        i+=1

        resp = requests.get(url + "&page=" + str(i),headers=B_HEADER)

    return orders

def get_request_Etsy_API_v2(url_ext, total):

    # API call Etsy to receive data
    etsy = OAuth1Session(ETSY_API_KEY, \
                            client_secret=ETSY_CLIENT_SECRET, \
                            resource_owner_key=ETSY_RESOURCE_OWNER_KEY, \
                            resource_owner_secret=ETSY_RESOURCE_OWNER_SECRET)

    url = ETSY_BASE_URL + url_ext

    i=1
    r_data = []
    
    resp = etsy.get(url + "&page=" + str(i))
    
    while 'json' in resp.headers.get('Content-Type') and 'results' in resp.json().keys() and i < total:

        
        # This means something went wrong.
        if resp.status_code != 200: 
            print("Something is wrong!!!")
        else:
            r_data.extend(resp.json()['results'])

        i+=1
        resp = etsy.get(url + "&page=" + str(i))
        

    return r_data

def update_orders():
    
    # Update orders with Etsy Data
    r_data = get_request_Etsy_API_v2('/shops/'+ETSY_SHOP_ID+'/receipts?limit=100&', 60)
    for r_receipts in r_data:
        order, created = Order.objects.get_or_create(order_id=r_receipts['receipt_id'])
        if created :
            order.first_name = r_receipts['name']

            order.region = r_receipts['state']
            order.address1 = r_receipts['first_line']
            order.city = r_receipts['city']
            order.zip_code = r_receipts['zip']

            order.email = r_receipts['buyer_email']
            order.country = r_receipts['country_id']

            order.total_price = r_receipts['grandtotal']
            order.total_tax = r_receipts['total_tax_cost']

            order.created_at = datetime.datetime.fromtimestamp(r_receipts['creation_tsz'], tz=pytz.UTC)
            order.save()

    # Update orders with Printify Data
    r_data = get_request_Printify_API('orders.json?limit=10&')

    for r_order in r_data:
        if 'shop_order_id' in r_order['metadata'].keys():
            order = Order.objects.filter(order_id=r_order['metadata']['shop_order_id']).first()
            if order :
                order.total_cost = round(float(r_order['total_price'] + r_order['total_shipping'])/100.0*1.24,2)
                order.save()

def update_listings(shop):
    "Creating new listing records for every listing that associated with shop."
    
    r_data = get_request_Etsy_API_v2('/shops/'+shop.name+'/listings/active?limit=100&', 100000)

    for r_listing in r_data:

        listing, created = Listing.objects.get_or_create(listing_id=r_listing['listing_id'])
        if created :
            listing.shop = shop 
            listing.title = r_listing['title']
            
            listing.original_creation_tsz = datetime.datetime.fromtimestamp(r_listing['original_creation_tsz'], tz=pytz.UTC)
            listing.save()

        listing_record = ListingRecord( \
                            listing=listing, \
                            price= float(r_listing['price']), \
                            quantity = int(r_listing['quantity']), \
                            views = int(r_listing['views']), \
                            num_favorers = int(r_listing['num_favorers']))
        listing_record.save()

def update_shops():
    "Update every shop"

    for shop in Shop.objects.all():
        update_listings(shop)