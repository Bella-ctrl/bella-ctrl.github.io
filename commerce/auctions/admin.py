from django.contrib import admin
from .models import User, Listings, Bids, Comments, Watchlist

# Register your models here.
class BasicAdmin(admin.ModelAdmin):
    list_display = ('__str__',)  # Just shows the string representation

admin.site.register(User, BasicAdmin)
admin.site.register(Listings, BasicAdmin)
admin.site.register(Bids, BasicAdmin)
admin.site.register(Comments, BasicAdmin)
admin.site.register(Watchlist, BasicAdmin)