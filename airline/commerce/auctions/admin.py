from django.contrib import admin

# Register your models here.
from .models import Listing, Bids, Comment, MatchList

admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Comment)
admin.site.register(MatchList)