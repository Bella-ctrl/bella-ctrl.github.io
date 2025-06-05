from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    CATEGORY_CHOICES = [
        ('ART', 'Art'),
        ('CLOTH', 'Clothing'),
        ('ELEC', 'Electronics'),
        ('HOME', 'Home'),
        ('SPORT', 'Sports'),
        ('TOYS', 'Toys'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=64)
    starting_bid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(
        max_length=5,
        choices=CATEGORY_CHOICES,
        blank=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings"
    )

    def __str__(self):
        return f"{self.title} (${self.starting_bid})"

class Bids(models.Model):
    listing = models.ForeignKey(
        Listings,
        on_delete=models.CASCADE,
        related_name="bids"
    )
    bid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    bidder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bids_made"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-bid_amount']
        get_latest_by = 'bid_amount'

    def __str__(self):
        return f"${self.bid_amount} on {self.listing.title}"

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
    comment_text = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    created_at = models.DateTimeField(auto_now_add=True)
