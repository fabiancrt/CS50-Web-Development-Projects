from django.contrib import admin
from .models import User, ProductListing, Offer, Review, Watchlist

# here are the extra admin pannel features i added

#the admin panel for product listing management
@admin.register(ProductListing)
class ProductListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'initial_price', 'highest_offer', 'category_name', 'active', 'owner', 'date_posted')
    list_filter = ('active', 'category_name', 'date_posted')
    search_fields = ('name', 'details', 'category_name', 'owner__username')
    ordering = ('-date_posted',)

#this is the admin panel for the offer management
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'offer_price', 'offerer', 'offer_date')
    list_filter = ('offer_date', 'offer_price')
    search_fields = ('product__name', 'offerer__username')
    ordering = ('-offer_date',)

#this , this is the admin panel for the reviews to be managed
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'review_text', 'reviewer', 'review_date')
    list_filter = ('review_date',)
    search_fields = ('product__name', 'reviewer__username', 'review_text')
    ordering = ('-review_date',)

#& finally for the watchlists to be managed
@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__name')

admin.site.register(User)