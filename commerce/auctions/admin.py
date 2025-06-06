from django.contrib import admin
from .models import User, Listings, Bids, Comments, Watchlist

# User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Listings Admin
class ListingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'starting_bid', 'category', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'owner__username', 'description')
    list_editable = ('is_active',)  # Allows editing directly from list view

# Bids Admin
class BidsAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'bid_amount', 'created_at')
    list_filter = ('created_at', 'listing__is_active')
    search_fields = ('listing__title', 'bidder__username')

# Comments Admin
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'created_at', 'short_text')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'listing__title')
    
    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Comment Preview'

# Watchlist Admin
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'listing__title')

# Register all your models here
admin.site.register(User, UserAdmin)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Watchlist, WatchlistAdmin)