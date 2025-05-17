from django.contrib import admin
from .models import User, Listing, Bid, Comment, WatchList

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'current_bid', 'category', 'is_active')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'amount', 'bid_time')
    list_filter = ('bid_time',)
    search_fields = ('listing__title', 'bidder__username')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'author', 'created_at', 'short_text')
    list_filter = ('created_at',)
    search_fields = ('text', 'listing__title')
    
    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Comment Preview'

class WatchListAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'listing__title')

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(WatchList, WatchListAdmin)