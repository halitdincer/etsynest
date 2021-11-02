from django.db import models

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

    total_price = models.FloatField(default=0,null=True, blank=True)
    total_shipping = models.FloatField(default=0,null=True, blank=True)
    total_tax = models.FloatField(default=0,null=True, blank=True)

    total_cost = models.FloatField(default=0,null=True, blank=True)

    status = models.CharField(max_length=20,null=True, blank=True)

    created_at = models.DateTimeField(blank=True, null=True)
    sent_to_production_at = models.DateTimeField(blank=True, null=True)
    fulfilled_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.first_name) + "'s Order"
    
    def as_json(self):
        return dict(
            order_id=self.order_id,
            first_name=self.first_name, 
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            total_price=self.total_price,
            total_cost=self.total_cost,
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
