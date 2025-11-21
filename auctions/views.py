from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import User, Listing, Bids, Comment,Category
from .forms import listingForm, commentForm, bidsForm
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "auctions/index.html",{
        "Listings": Listing.objects.filter(is_active=True)
    })


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
    
@login_required
def create(request):
    if request.method == 'POST':
        form = listingForm(request.POST)
        if form.is_valid():
            Listing = form.save(commit=False) # dont save yet
            Listing.current_bid = Listing.starting_bid
            Listing.createdby = request.user
            Listing.save()
            return HttpResponseRedirect(reverse(index))
        
    else:
        form = listingForm()

    return render(request, "auctions/create.html",{
        'form': form
    })

@login_required
def place_bid(request, listing_id):
    form1 = bidsForm()
    form2 = commentForm()
    listing = get_object_or_404(Listing, pk=listing_id)
    user = request.user
    
    if request.method == 'POST':
        if "bid_amount" in request.POST:
            form1 = bidsForm(request.POST)
            if form1.is_valid():
                amount = form1.cleaned_data["amount"]
                if float(amount) > listing.current_bid:
                    Bids.objects.create(listing=listing, amount=amount, bidder=request.user)
                    listing.current_bid = amount
                    listing.save()
                    return HttpResponseRedirect(reverse('place_bid', args=[listing_id]))
                else:
                    return render(request, "auctions/place_bid.html",{
                        "error": "Amount must higher than the current price",
                        "listing": listing,
                        "form1": form1,
                        "form2":form2,
                    })
        elif "add_comment" in request.POST:
            form2 = commentForm(request.POST)
            if form2.is_valid():
                comment = form2.cleaned_data["comment"]
                Comment.objects.create(listing=listing, user=request.user, comment=comment)
                return HttpResponseRedirect(reverse('place_bid', args=[listing_id]))
            else:
                return render (request, "auctions/place_bid.html",{
                    "error": "invalid comment",
                    "listing": listing,
                    "form2": form2
                })
        
    return render(request, "auctions/place_bid.html",{
        "form1":form1,
        "listing": listing,
        "Comments": Comment.objects.filter(listing=listing),
        "form2": form2,
        "user": user,
        "Bids": Bids.objects.filter(listing=listing).order_by('-amount'),
    })


def category(request):
    return render(request, "auctions/category.html",{
        "Categories":Category.objects.all()
    });

def category_items(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, "auctions/category_items.html", {
        "Listings": Listing.objects.all(),
        "category": category
    })

@login_required
def watchlist(request):
    user = request.user
    items = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "items":items
    })

def add_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    user = request.user

    if listing in user.watchlist.all():
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)
    return redirect('place_bid', listing_id)


def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    if request.user == listing.createdby:
        highest_bid = listing.bids.order_by("-amount").first()

        if highest_bid:
            listing.winner = highest_bid.bidder

        listing.is_active = False
        listing.save()

    return redirect('place_bid', listing_id)

def my_listings(request):
    listings = Listing.objects.filter(createdby=request.user)
    return render(request, "auctions/my_listings.html",{
        "listings": listings
    })

def won_auctions(request):
    listings = Listing.objects.filter(winner=request.user)
    return render(request, "auctions/won_auctions.html", {
        "listings": listings
    })



