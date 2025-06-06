from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import User, Listings, Bids, Comments, Watchlist

class CreateForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'starting_bid', 'description', 'image_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(is_active=True)
    })

#Active Listings Page: The default route of your web application 
#should let users view all of the currently active auction listings. 
#For each active listing, this page should display (at minimum) 
#the title, description, current price, and photo (if one exists for the listing).



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


def create_listing(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            
            messages.success(request, "Listing created successfully!")
            return redirect('index')
            
    else:
        form = CreateForm()
    
    return render(request, "auctions/create_listing.html", {
        "form": form,
        "title": "Create New Listing"
    })

def listing(request, listing_id):
    try:
        listing = Listings.objects.get(id=listing_id)
        comments = Comments.objects.filter(listing=listing).order_by('-created_at')
        bids = Bids.objects.filter(listing=listing).order_by('-bid_amount')
        
        # Get current price (highest bid or starting bid)
        current_price = bids.aggregate(Max('bid_amount'))['bid_amount__max'] or listing.starting_bid
        
        # Check watchlist status
        on_watchlist = False
        if request.user.is_authenticated:
            on_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
            
            # Check if user is winner
            is_winner = False
            if not listing.is_active and bids.exists():
                highest_bid = bids.first()
                is_winner = highest_bid.bidder == request.user
            
        context = {
            'listing': listing,
            'comments': comments,
            'bids': bids,
            'current_price': current_price,
            'on_watchlist': on_watchlist,
            'is_owner': request.user == listing.owner,
            'is_winner': is_winner if request.user.is_authenticated else False,
            'title': listing.title
        }
        
        return render(request, "auctions/listing.html", context)
        
    except Listings.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Listing not found."
        })

@login_required
def watchlist_toggle(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)
    
    if Watchlist.objects.filter(user=request.user, listing=listing).exists():
        Watchlist.objects.filter(user=request.user, listing=listing).delete()
        messages.success(request, "Removed from watchlist")
    else:
        Watchlist.objects.create(user=request.user, listing=listing)
        messages.success(request, "Added to watchlist")
    
    return redirect('listing', listing_id=listing_id)

@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)
    
    if request.method == "POST":
        bid_amount = float(request.POST.get('bid_amount'))
        current_price = Bids.objects.filter(listing=listing).aggregate(Max('bid_amount'))['bid_amount__max'] or listing.starting_bid
        
        if bid_amount < listing.starting_bid:
            messages.error(request, "Bid must be at least the starting price")
        elif bid_amount <= current_price:
            messages.error(request, "Bid must be higher than current price")
        else:
            Bids.objects.create(
                listing=listing,
                bidder=request.user,
                bid_amount=bid_amount
            )
            messages.success(request, "Bid placed successfully!")
    
    return redirect('listing', listing_id=listing_id)

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id, owner=request.user)
    
    if listing.is_active:
        listing.is_active = False
        listing.save()
        messages.success(request, "Auction closed successfully")
    
    return redirect('listing', listing_id=listing_id)

@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)
    
    if request.method == "POST":
        text = request.POST.get('comment_text')
        if text:
            Comments.objects.create(
                listing=listing,
                user=request.user,
                text=text
            )
            messages.success(request, "Comment added")
    
    return redirect('listing', listing_id=listing_id)

@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user).select_related('listing')
    
    listings = [item.listing for item in watchlist_items]

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "title": "Your Watchlist"
    })

def categories(request):
    # Get all distinct categories that have active listings
    categories = Listings.objects.filter(is_active=True)\
                      .exclude(category__isnull=True)\
                      .values_list('category', flat=True)\
                      .distinct()
    
    # Convert to human-readable format with counts
    category_list = []
    for code, name in Listings.CATEGORY_CHOICES:
        count = Listings.objects.filter(is_active=True, category=code).count()
        if count > 0:
            category_list.append({
                'code': code,
                'name': name,
                'count': count
            })
    
    return render(request, "auctions/categories.html", {
        "categories": category_list,
        "title": "All Categories"
    })

def category_listings(request, category_code):
    # Get human-readable category name
    category_name = dict(Listings.CATEGORY_CHOICES).get(category_code, "Unknown")
    
    listings = Listings.objects.filter(
        is_active=True,
        category=category_code
    ).order_by('-created_at')
    
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category_name": category_name,
        "category_code": category_code,
        "title": f"Category: {category_name}"
    })
