from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auctions(models.Model):
    ACCESSORIES = "Accessories"
    AUTOMOTIVE = "Automotive"
    BOOKS = "Books"
    COMPUTERS = "Computers"
    ELECTRONICS = "Electronics"
    FASHION = "Fashion"
    FURNITURE = "Furniture"
    GROCERIES = "Groceries"
    HEALTH = "Health"
    HOME_DECOR = "Home Decor"
    KITCHEN = "Kitchen"
    OFFICE_SUPPLIES = "Office Supplies"
    PERFUMES = "Perfumes"
    SPORTS_FITNESS = "Sports and Fitness"
    TOOLS = "Tools"
    TOYS = "Toys"
    VIDEO_GAMES = "Video Games"

    CATEGORIES = [
        (ACCESSORIES, "Accessories"),
        (AUTOMOTIVE, "Automotive"),
        (BOOKS, "Books"),
        (COMPUTERS, "Computers"),
        (ELECTRONICS, "Electronics"),
        (FASHION, "Fashion"),
        (FURNITURE, "Furniture"),
        (GROCERIES, "Groceries"),
        (HEALTH, "Health"),
        (HOME_DECOR, "Home Decor"),
        (KITCHEN, "Kitchen"),
        (OFFICE_SUPPLIES, "Office Supplies"),
        (PERFUMES, "Perfumes"),
        (SPORTS_FITNESS, "Sports and Fitness"),
        (TOOLS, "Tools"),
        (TOYS, "Toys"),
        (VIDEO_GAMES, "Video Games"),
]
    Title = models.CharField(max_length=50)
    Description = models.CharField(max_length=500, blank=True)
    Price = models.DecimalField(max_digits=25, decimal_places=2)
    Category = models.CharField(max_length=50, choices=CATEGORIES,)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    Status = models.BooleanField(default=False)
    Seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Sellers")
    Bid = models.ManyToManyField("Bids", blank=True, related_name="Bids") 
    Comment = models.ManyToManyField("Comments", blank=True, related_name="Comments") 
    Watch = models.ManyToManyField("Watchlist", blank=True, related_name="watchlist") 
    Image = models.ImageField(null=True, blank=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Watcher")
    Watchlisted = models.ForeignKey(Auctions, default=None, on_delete=models.CASCADE, related_name="watchlist", unique= True)

class Comments(models.Model):
    Com = models.ForeignKey(Auctions, default=None, on_delete=models.CASCADE, related_name="Comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    title = models.CharField(max_length=50, default="")
    comment = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True, blank=True)

class Bids(models.Model):
    time = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Bid = models.ForeignKey(Auctions, default=None, on_delete=models.CASCADE)

class Winner(models.Model):
    Bidwinner = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="Winner")
    Listiing = models.ForeignKey(Auctions, default=None, on_delete=models.CASCADE, related_name="Auction")