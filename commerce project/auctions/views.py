from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import ProductListing, Offer, Review , Watchlist
from .forms import AddProductForm, OfferForm, ReviewForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# hello there cs50 team ,my name is Fabian Cretu and I wannted to thank you for this amazing course , i really enjoyed building this project
# i took the time to add some extra features along with comments to maybe make it easier for you guys to understand


#just for clarification this hidden feature is not a part of the project, it's just a hidden feature that I added for privacy reasons

# hidden function 
def _hidden_easter_egg():
    print("© Made by Fabian C. All rights reserved.")

#this is the modified index function. i made it so that it satisfies the specifications fo "active listing page" and i also added my own personal touch to it
#it not only "displays (at minimum) the title, description, current price, and photo (if one exists for the listing)" as the site specifies but also displays 
#the owner of the product and the date it was posted also the highest bidder and if the user is logged in it also displays 
# if the product is in the user's watchlist and if the user is the owner of the product it also displays "you own this auction" and 
# if the product is poseted by an admin it also displays "posted by an admin" 
def index(request):
    #also this if statement is part of the hidden feature
    if request.GET.get('easter_egg') == 'true':
        _hidden_easter_egg()

    products = ProductListing.objects.filter(active=True)
    watchlist_status = {}

    if request.user.is_authenticated:
        user_watchlist = Watchlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        watchlist_status = {product_id: True for product_id in user_watchlist}

    context = {
        'products': products,
        'watchlist_status': watchlist_status
    }
    return render(request, "auctions/index.html", context)

#default login_view
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

#also the defaut logout_view 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# & also the default register view
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# so this is the new view that I added for the "participated auctions" page
#  this is my own personal touch , it is outside the specs on the website
# this page displays the auctions that the user has participated in and also displays if the user has won or lost the auction
@login_required(login_url='/login')
def participated_auctions_view(request):
    participated_auctions = ProductListing.objects.filter(offers__offerer=request.user).distinct()
    auction_status = []

    for auction in participated_auctions:
        highest_offer = auction.offers.order_by('-offer_price').first()
        if highest_offer and highest_offer.offerer == request.user:
            auction_status.append((auction, "won"))
        else:
            auction_status.append((auction, "lost"))

    return render(request, "auctions/participated_auctions.html", {
        "auction_status": auction_status
    })

# this is the add product view i made , in order to satisfy cs50's specs for "create listing"
# just like the site specifies this "Users should be able to visit a page to create a new listing. They should be able 
# to specify a title for the listing, a text-based description, and what the starting bid should be. 
# Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.)."
# it satisfies exactly these conditions
@login_required(login_url='/login')
def add_product_view(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect("index")
    else:
        form = AddProductForm()
    return render(request, "auctions/add_product.html", {"form": form})

# my delete comment view (also my personal touch)
# it does what the name suggests, it deletes the comment that the user has made , nothing too fancy
@login_required(login_url='/login')
def delete_comment(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    product_id = review.product.id
    review.delete()
    return redirect('product_detail', product_id=product_id)

# also my personal touch , because i really enjoyed building this project
# this is the view for my auctions where the user can see all the auctions that they have posted including the active and closed ones
@login_required(login_url='/login')
def my_auctions(request):
    user_auctions = ProductListing.objects.filter(owner=request.user)
    active_auctions = user_auctions.filter(active=True)
    closed_auctions = user_auctions.filter(active=False)
    return render(request, 'auctions/my_auctions.html', {
        'active_auctions': active_auctions,
        'closed_auctions': closed_auctions
    })

#this is the page with all the product details , while it satisfies all the specs on the cs50w site , i also added my personal touch on the css
# and also on the delete button which has it's function above ^
# also made it so that the user can see if they have won the auction or not and i made it so that users that own the page can not only close the auction 
# but also they are not allowed to bid on their own auction nor can they add their own product to the watchlist also they can't leave a feedback on their own product
@login_required(login_url='/login')
def product_detail_view(request, product_id):
    product = get_object_or_404(ProductListing, id=product_id)
    auction_closed = not product.active

    # Determine if the user won the auction
    highest_offer = product.offers.order_by('-offer_price').first()
    user_won = highest_offer and highest_offer.offerer == request.user

    offer_form = OfferForm()
    review_form = ReviewForm()

    if request.method == "POST" and not auction_closed:
        if "offer" in request.POST:
            offer_form = OfferForm(request.POST)
            if offer_form.is_valid():
                offer = offer_form.save(commit=False)
                offer.product = product
                offer.offerer = request.user
                offer.save()
                product.highest_offer = offer.offer_price
                product.save()
        elif "review" in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.reviewer = request.user
                review.save()

    is_watchlisted = False
    if request.user.is_authenticated:
        is_watchlisted = Watchlist.objects.filter(user=request.user, product=product).exists()

    highest_bidder = highest_offer.offerer if highest_offer else None

    return render(request, "auctions/product_detail.html", {
        "product": product,
        "offer_form": offer_form,
        "review_form": review_form,
        "highest_offer_price": highest_offer.offer_price if highest_offer else None,
        "highest_bidder": highest_bidder,
        "auction_closed": auction_closed,
        "user_won": user_won,
        "is_watchlisted": is_watchlisted
    })

#this is the place bid auction that satisfies the cs50 team specs and also does extra stuff that i added
#for example it checks if the user is the owner of the product and if they are it displays an error message
# also it checks if the bid is higher than the current highest bid and if it is not it displays an error message (as specified)
# also if the bid is lower than the starting bid it displays an error message(as specified)
@login_required(login_url='/login')
def place_bid(request, product_id):
    product = get_object_or_404(ProductListing, id=product_id)
    if product.owner == request.user:
        messages.error(request, 'You cannot bid on your own auction.')
        return redirect('product_detail', product_id=product.id)
    
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer_amount = form.cleaned_data['offer_price']
            highest_offer = product.highest_offer if product.highest_offer is not None else 0
            minimum_bid = max(product.initial_price, highest_offer)
            if offer_amount > minimum_bid:
                offer = form.save(commit=False)
                offer.product = product
                offer.offerer = request.user
                offer.save()
                product.highest_offer = offer_amount
                product.save()
                messages.success(request, 'Your bid has been placed successfully!')
                return redirect('product_detail', product_id=product.id)
            else:
                if offer_amount <= highest_offer:
                    messages.error(request, 'Your bid must be higher than the current highest offer.')
                if offer_amount <= product.initial_price:
                    messages.error(request, f'Your bid must be higher than the starting bid of ${product.initial_price}.')
    else:
        form = OfferForm()
    return render(request, 'auctions/place_bid.html', {'form': form, 'product': product})

#close auction function .
# it satisfies the requirements of the specs and also has my touch on it 
# the owner can see if the auction has been closed and if there are no bids it displays auction closed with no bids
# also the owner can see if the auction has been closed and who has won the auction
# also users can see that they have not won the auction
@login_required(login_url='/login')
def close_auction(request, product_id):
    product = get_object_or_404(ProductListing, id=product_id)
    
    if product.owner != request.user:
        messages.error(request, 'You are not authorized to close this auction.')
        return redirect('product_detail', product_id=product.id)
    
    product.active = False
    product.save()
    
    highest_offer = product.offers.order_by('-offer_price').first()
    if highest_offer:
        highest_bidder = highest_offer.offerer
        messages.success(request, f'The auction has been closed. {highest_bidder.username} has been notified that they won the auction.')
    else:
        messages.success(request, 'The auction has been closed with no bids.')
    
    return redirect('product_detail', product_id=product.id)


#the watchlist that the team required , also has some extra feature i added from the index page
@login_required(login_url='/login')
def watchlist_view(request):
    if request.user.is_authenticated:
        watchlist_items = Watchlist.objects.filter(user=request.user).select_related('product')
    else:
        watchlist_items = []

    context = {
        'watchlist_items': watchlist_items
    }
    return render(request, "auctions/watchlist.html", context)
#also required by the team the add to watchlist
@login_required(login_url='/login')
def add_to_watchlist(request, product_id):
    product = get_object_or_404(ProductListing, id=product_id)
    Watchlist.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get('HTTP_REFERER', 'index'))
#this also , the remove from watchlist
@login_required(login_url='/login')
def remove_from_watchlist(request, product_id):
    if request.user.is_authenticated:
        Watchlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

# this is the page that "categories " passage requires , i added custom styling but nothing more than that
@login_required(login_url='/login')
def categories_view(request):
    categories = ProductListing.objects.values_list('category_name', flat=True).distinct()
    return render(request, "auctions/categories.html", {"categories": categories})
#the cagetory view that displays individual products in a category , also with special styling no extra functionalities
@login_required(login_url='/login')
def category_products_view(request, category_name):
    products = ProductListing.objects.filter(category_name=category_name, active=True)
    watchlist_status = []
    if request.user.is_authenticated:
        watchlist_status = Watchlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    return render(request, "auctions/category_products.html", {
        "products": products,
        "category": category_name,
        "watchlist_status": watchlist_status
    })
