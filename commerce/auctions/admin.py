from django.contrib import admin

from .models import Auctions, Comments, Bids, Watchlist

# Register your models here.
admin.site.register(Auctions)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(Watchlist)