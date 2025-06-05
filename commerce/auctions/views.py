from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Bids, Comments


class CreateForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=64,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter listing title'
        })
    )
    
    starting_bid = forms.DecimalField(
        label="Starting Bid ($)",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe your item...'
        }),
        required=False
    )
    
    image_url = forms.URLField(
        label="Image URL",
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com/image.jpg'
        }),
        required=False
    )
    
    CATEGORY_CHOICES = [
        ("", "Select a category"),  
        ("Art", "Art"),
        ("Clothing", "Clothing"),
        ("Electronics", "Electronics"),
        ("Home", "Home"),
        ("Sports", "Sports"),
        ("Toys", "Toys"),
        ("Other", "Other"),
    ]
    
    category = forms.ChoiceField(
        label="Category",
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

def index(request):
    return render(request, "auctions/index.html")


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
            title = form.cleaned_data["title"]
            starting_bid = form.cleaned_data["starting_bid"]
            description = form.cleaned_data["description"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]

            # Create a new listing
            listing = Listings(
                title=title,
                starting_bid=starting_bid,
                description=description,
                image_url=image_url,
                category=category,
                owner=request.user
            )
            listing.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })      
    else:
        return render(request, "auctions/create_listing.html", {
            "form": CreateForm()
        })
