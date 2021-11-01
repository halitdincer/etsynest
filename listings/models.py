from django.db import models
from django.utils.timezone import now

class Listing(models.Model):
    listing_id = models.CharField(max_length=60, default="")
    shop = models.ForeignKey('shops.Shop', null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=600)

    original_creation_tsz = models.DateTimeField(default=now, blank=True)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return "Title:"+self.title

class ListingRecord(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    num_favorers = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.listing.title + "(" + str(self.created_at) + ")"