from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Auctions, Watchlist, Comments, Bids, Winner
from datetime import datetime
from django.shortcuts import get_object_or_404

@login_required
def index(request):
    if request.method == "GET":
        List = Auctions.objects.filter(Status = True)
        return render(request, "auctions/index.html", {"List": List, "foo": "Active Listings"}) 
    
@login_required
def closedaucts(request):
    if request.method == "GET":
        List = Auctions.objects.filter(Status = False)
        return render(request, "auctions/index.html", {"List": List, "foo": "Closed Listings"}) 

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

@login_required
def categories(request):
    if request.method == "POST":
        Searched = request.POST.get("Categories")
        List = Auctions.objects.filter(Status = True).filter(Category = Searched)
        return render(request, "auctions/index.html", {"List": List, "Searched": Searched}) 
    return render(request, "auctions/categories.html")

        
@login_required
def watchlist(request):
    if request.method == "GET":
        Watch = Watchlist.objects.all().filter(user = request.user)
        return render(request, "auctions/watchlist.html", {"Watchlist": Watch})
    else:
        ID = int(request.POST.get("id"))
        List = Auctions.objects.get(pk=ID)
        Watch = Watchlist.objects.all().filter(Watchlisted = ID)
        Len = len(Watch)
        if Len == 0:
            temp = Watchlist(
                user = User.objects.get(username= request.user),
                Watchlisted = List
            )
            temp.save()
            return redirect("watchlist")
        Watch = Watchlist.objects.all()
        List = Auctions.objects.filter(pk = ID)
        return render(request, "auctions/view.html", {"List": List, "Watch": Watch, "Len": Len})

@login_required
def create(request):
    if request.method == "POST":
        Title = request.POST.get("Title")
        Desc = request.POST.get("Desc")
        Price = request.POST.get("Price")
        Image = request.POST.get("Image")
        Category = request.POST.get("Categories")
        Status = request.POST.get("Status")
        time = datetime.today().replace(microsecond=0)

        if Title == None or Title == "" or Desc == None or Desc == "" or Price == None or Price == "" or Category == None or Category == "" or Status == None or Status == "": 
            error ="All fields are required"
            return render(request, "auctions/create.html", {"error": error})
        else:
            List = Auctions(
                Title = Title,
                Description = Desc,
                Price = Price,
                Category = Category,
                Image = Image,
                Status = Status,
                Seller = User.objects.get(username= request.user),
                time = time,
            )
            List.save()
            return redirect("index")
    return render(request, "auctions/create.html")
        

@login_required
def view(request):
    if request.method == "POST":
        title = request.POST.get("Title")
        List = Auctions.objects.filter(Title = title)
        Len = len(Watchlist.objects.all().filter(Watchlisted = List.get().pk))
        return render(request, "auctions/view.html", {
            "List": List, 
            "User": User.objects.get(username = request.user),
            "Comment": Comments.objects.all(), 
            "Bids": Bids.objects.all(),
            "Watchlist": Watchlist.objects.all(),
            "Winner": Winner.objects.all(),
            "Len": Len,
        })
    return redirect("index")

@login_required
def comment(request):
    if request.method =="POST":
        Time = datetime.today().replace(microsecond=0)
        ID = request.POST.get("id")
        Title = request.POST.get("Title")
        Comment = request.POST.get("comment")
        Com = Auctions.objects.get(pk=ID)
        if Title != None and Title != "" and Comment != "" and Comment != None:
            temp = Comments(
                Com = Com,
                title = Title,
                comment = Comment,
                user = User.objects.get(username= request.user),
                time = Time,
            )
            temp.save()
            message = "Comment added Successfully"
            return render(request, "auctions/view.html", {"message":message})
        message = "Invalid Title and/or Comment."
        return render(request, "auctions/view.html", {"message":message})

@login_required    
def bid(request):
    if request.method =="POST":
        ID = request.POST.get("id")
        amountbid = request.POST.get("Bid")
        bid = Auctions.objects.get(pk=ID)
        Time = datetime.today().replace(microsecond=0)
        price = Auctions.objects.get(pk = ID).Price
        allbids = Bids.objects.all().filter(Bid = ID)
        if amountbid == None or amountbid == "":
            message = "Please enter a valid bid amount"
            return render(request, "auctions/view.html", {"message":message})
        amountbid = float(amountbid)
        if amountbid < float(price):
            message = "Bid cannot be lower than price of item"
            return render(request, "auctions/view.html", {"message":message})
        else:
            for i in allbids:
                if amountbid < float(i.price):
                    message = "Bid cannot be lower than any previous bids"
                    return render(request, "auctions/view.html", {"message":message})
                
        if bid.Seller != User.objects.get(username =request.user):
            temp = Bids(
                time =Time,
                user = User.objects.get(username= request.user),
                price = amountbid,
                Bid = bid,
            )
            temp.save()
            message = "Bid added Successfully"
            return render(request, "auctions/view.html", {"message":message})
        else:
            return render(request, "auctions/view.html", {"User": User.objects.get(user = request.user)})
            

@login_required
def remove(request):
    if request.method == "POST":
        ID = request.POST.get("id")
        Watch = Watchlist.objects.get(Watchlisted = ID)
        Watch.delete()
        Watch = Watchlist.objects.all().filter(user = request.user)
        return redirect("watchlist") 


@login_required
def close(request):
    if request.method == "POST":
        ID = request.POST.get("id")
        List = Auctions.objects.get(pk=ID)
        List.Status = False
        List.save()

        if len(Bids.objects.all().values("price").filter(Bid = ID)) != 0:
            temp = Bids.objects.all().filter(Bid = ID)
            highestBid = Bids.objects.all().filter(Bid = ID)[0]
            for i in temp:
                if highestBid.price < i.price:
                    highestBid = i

            foo = Bids.objects.all().filter(price = highestBid.price)

            Win = Winner(
                Bidwinner = foo.get().user,
                Listiing = List
            )
            Win.save()
            return redirect("index") 
        else:
            return redirect("index") 
