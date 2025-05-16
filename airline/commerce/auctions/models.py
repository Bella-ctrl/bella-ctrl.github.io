from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# App should have at least three models: auction listings, bids, and comments made on auction listings
# Auction listings model
class Auction(models.Model):
    pass

# Bids model
class Bids(models.Model):
    pass

# Comments on Auctions listings 
class Comments(models.Model):
    pass