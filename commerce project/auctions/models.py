from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#here according to the first step, I had to make three models except the one above ^^
#so I made productlisting(for auction listing) & offer(for bid)  the review(for comment) and also watchlist(for the watchlist)
class ProductListing(models.Model):
    name = models.CharField(max_length=64)
    details = models.TextField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    highest_offer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_link = models.URLField(blank=True)
    category_name = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

class Offer(models.Model):
    product = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name="offers")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    offerer = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_date = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    product = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name="reviews")
    review_text = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review_date = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    product = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name="watchlisted_by")

    class Meta:
        unique_together = ('user', 'product')


