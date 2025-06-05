from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


from .models import User, Listings, Bids, Comments

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
        "listings": Listings.objects.all()
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
    if request.method == "POST":
        pass
    else:
        listing = Listings.objects.get(id=listing_id)
        comments = Comments.objects.filter(listing=listing)
        bids = Bids.objects.filter(listing=listing).order_by('-bid_amount')
        
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "bids": bids,
        })
