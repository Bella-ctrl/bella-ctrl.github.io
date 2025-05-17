from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import User, Listing, WatchList, Comment, Bid

def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
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

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'category': forms.Select(choices=Listing.CATEGORY_CHOICES),
        }
        
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():  
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return redirect("index")
    else:
        form = CreateListingForm()
    
    return render(request, "auctions/create.html", {
        "form": form
    })


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    in_watchlist = False
    is_creator = False
    is_winner = False
    comments = Comment.objects.filter(listing=listing).order_by('-created_at')

    if request.user.is_authenticated:
        in_watchlist = WatchList.objects.filter(user=request.user, listing=listing).exists()
        is_creator = request.user == listing.creator
        is_winner = request.user == listing.winner
    
    if request.method == "POST" and request.user.is_authenticated:
        if 'watchlist' in request.POST:
            if in_watchlist:
                WatchList.objects.filter(user=request.user, listing=listing).delete()
                messages.success(request, "Removed from your watch-list")
            else:
                WatchList.objects.create(user=request.user, listing=listing)
                messages.success(request, "Added to your watch-list")
            return redirect('listing_detail', listing_id=listing.id)
        
        elif 'bid' in request.POST:
            bid_amount = float(request.POST.get('bid_amount', 0))
            if bid_amount >= listing.starting_bid and (listing.current_bid is None or bid_amount > listing.current_bid):
                Bid.objects.create(
                    bidder=request.user,
                    listing=listing,
                    amount=bid_amount
                )
                listing.current_bid = bid_amount
                listing.save()
                messages.success(request, "Bid placed successfully!")
            else: 
                messages.error(request, "Bid must be higher than current price")
            return redirect('listing_detail', listing_id=listing.id)
        
        elif 'close' in request.POST and is_creator:
            if listing.current_bid:
                listing.winner = Bid.objects.filter(listing=listing).order_by('-amount').first().bidder
            listing.is_active = False
            listing.save()
            messages.success(request, "Auction closed successfully!")
            return redirect('listing_detail', listing_id=listing.id)
        
        elif 'comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                Comment.objects.create(
                    author=request.user,
                    listing=listing, 
                    text=form.cleaned_data['text']
                )
                messages.success(request, "Comment added!")
                return redirect('listing_detail', listing_id=listing.id)
    
    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "in_watchlist": in_watchlist,
        "is_creator": is_creator,
        "is_winner": is_winner,
        "comments": comments,
        "comment_form": CommentForm()
    })