from django.db import models
import math

class Order(models.Model):
    order_id = models.CharField(max_length=60)

    first_name = models.CharField(max_length=60,null=True, blank=True)
    last_name = models.CharField(max_length=60,null=True, blank=True)

    region = models.CharField(max_length=100,null=True, blank=True)
    address1 = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    zip_code = models.CharField(max_length=10,null=True, blank=True)

    email = models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=20,null=True, blank=True)

    country = models.CharField(max_length=10,null=True, blank=True)

    # Sum of The Individual Listings without tax and shipping
    total_price = models.FloatField(default=0,null=True, blank=True)
    total_discount = models.FloatField(default=0,null=True, blank=True)

    # Shipping Costs
    total_shipping_cost = models.FloatField(default=0,null=True, blank=True)

    # Necessary Costs
    total_tax_cost = models.FloatField(default=0,null=True, blank=True)
    total_vat_cost = models.FloatField(default=0,null=True, blank=True)

    # Summary of the Etsy Receipt
    subtotal = models.FloatField(default=0,null=True, blank=True) # total_price - discount without tax and shipping
    grandtotal = models.FloatField(default=0,null=True, blank=True) # total_price -discount with tax and shipping
    adjusted_grandtotal = models.FloatField(default=0,null=True, blank=True) # grandtotal after any adjusment to receipt

    # Printify Costs
    total_production_cost = models.FloatField(default=0,null=True, blank=True)

    status = models.CharField(max_length=20,null=True, blank=True)

    created_at = models.DateTimeField(blank=True, null=True)
    sent_to_production_at = models.DateTimeField(blank=True, null=True)
    fulfilled_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.first_name) + "'s Order"

    @property
    def estimated_item_count(self):
        count = self.subtotal/30
        if count < 1:
            count = 1
        return int(count)

    @property
    def processing_fees(self):
        rate = 5 ;
        if self.country == "209" or self.country == "79" :
            rate = 4 ;
        return (self.grandtotal*rate/100)+0.25

    @property
    def transaction_fees(self):
        return self.subtotal*5/100
    
    @property
    def shipping_transaction_fees(self):
        return self.total_shipping_cost*5/100

    @property
    def listing_fees(self):
        return self.estimated_item_count * 0.25

    @property
    def total_fees(self):
        return self.transaction_fees + self.listing_fees + self.processing_fees + self.shipping_transaction_fees
    
    @property
    def revenue(self):
        return int(self.total_production_cost != 0)*(self.subtotal+self.total_shipping_cost-self.total_fees-self.total_production_cost)
    
    def as_json(self):
        return dict(
            # Order Info
            order_id=self.order_id,
            first_name=self.first_name, 
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            country=self.country,
            # Item Count
            estimated_item_count=self.estimated_item_count,
            # Listing Price Fees and Discount / without tax and shipping
            total_price=self.total_price,
            total_discount=self.total_discount,
            # Shipping Cost
            total_shipping_cost=self.total_shipping_cost,
            # Tax 
            total_tax_cost=self.total_tax_cost,
            total_vat_cost=self.total_vat_cost,
            # Fees
            processing_fees=self.processing_fees,
            transaction_fees=self.transaction_fees,
            shipping_transaction_fees=self.shipping_transaction_fees,
            listing_fees=self.listing_fees,
            total_fees=self.total_fees,
            # Receipt Summary
            subtotal=self.subtotal,
            grandtotal=self.grandtotal,
            adjusted_grandtotal=self.adjusted_grandtotal,
            revenue=self.revenue,
            total_production_cost=self.total_production_cost,
            # Dates
            created_at=self.created_at.isoformat())

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    product_id = models.CharField(max_length=60)

    quantity = models.PositiveIntegerField(default=0)
    variant_id = models.PositiveIntegerField(default=0)
    print_provider_id = models.PositiveIntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    shipping_cost = models.PositiveIntegerField(default=0)

    title = models.CharField(max_length=60)
    variant_label = models.CharField(max_length=60)

    sent_to_production_at = models.DateTimeField(blank=True, null=True)
    fulfilled_at = models.DateTimeField(blank=True, null=True)

    quantity = models.PositiveIntegerField(default=0)
