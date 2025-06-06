from django.contrib import admin
from .models import User, Listings, Bids, Comments, Watchlist

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser')

@admin.register(Listings)
class ListingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'starting_bid', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'owner__username')

@admin.register(Bids)
class BidsAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'bid_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('listing__title', 'bidder__username')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'created_at')
    search_fields = ('text', 'user__username')

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'added_at')
    list_filter = ('added_at',)