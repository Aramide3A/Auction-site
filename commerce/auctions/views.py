from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from.forms import *
from .models import User
from .models import *
from django.contrib.auth.decorators import login_required


def index(request):
    lists = Listing.objects.all()
    context = {
        'lists': lists,
    }
    return render(request, "auctions/index.html", context)

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
def New_listing(request):
    if request.method == 'POST':
        form = Listing_form(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))

    form = Listing_form()
    context = {
        'form' : form,
    }
    return render(request, "auctions/new_listing.html", context)

@login_required
def listing_view(request, pk):
    lists = Listing.objects.get(id=pk)
    if request.method == 'POST':
        form = Bid_Form(request.POST)
        if form.is_valid():
            if lists.current_bid != None:
                if int(request.POST['amount'] )> int(lists.starting_bid) and int(request.POST['amount']) > int(lists.current_bid):
                    form = Bid_Form(request.POST)
                    i = form.save(commit=False)
                    i.user = request.user
                    i.listing = lists
                    i.save()
                    lists.current_bid = request.POST['amount']
                    context = {
                        'lists': lists,
                        'form' : Bid_Form(),
                    }
                    return render(request, "auctions/listing.html", context)
            else:
                if int(request.POST['amount'] )> int(lists.starting_bid) :
                    form = Bid_Form(request.POST)
                    i = form.save(commit=False)
                    i.user = request.user
                    i.listing = lists
                    i.save()
                    lists.current_bid = request.POST['amount']
                    context = {
                        'lists': lists,
                        'form' : Bid_Form(),
                    }
                    return render(request, "auctions/listing.html",context)
    form = Bid_Form()
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=lists)
    context = {
        'lists': lists,
        'form' : form,
        'comment_form' : comment_form,
        'comments': comments,

    }
    return render(request, "auctions/listing.html", context)

@login_required
def add_watchlist(request, pk):
    item = Listing.objects.get(id=pk)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.listing.add(item)
    lists = Listing.objects.get(id=pk)
    form = Bid_Form()
    context = {
        'lists': lists,
        'form': form,
        'message': 'Item successfully added to watchlist',
    }
    return render(request, "auctions/listing.html", context)

@login_required
def remove_watchlist(request, pk):
    item = Listing.objects.get(id=pk)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.listing.remove(item)
    lists = Listing.objects.get(id=pk)
    form = Bid_Form()
    context = {
        'lists': lists,
        'form': form,
        'message': 'Item successfully removed from watchlist',
    }
    return render(request, "auctions/listing.html", context)

@login_required
def close_bid(request, pk):
    item = Listing.objects.get(id=pk)
    item.completed = True
    item.save()
    context = {
        'winner_bid': item.current_bid
    }
    return redirect('listing', pk)

@login_required
def  comment(request,pk):
    listing = Listing.objects.get(id = pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.listing = listing
            new_comment.save()
            return redirect('listing', pk)
    else:
        form = CommentForm()
    return render(request, "auctions/listing.html")

@login_required
def watchlist(request):
    user_watchlist =  Watchlist.objects.get(user= request.user)
    watchlist = user_watchlist.listing.all()
    context = {
        'watch': watchlist,
    }
    return render(request, 'auctions/watchlist.html', context)

def category(request):
    lists = Listing.categories
    context = {
        'lists': lists
    }
    return render(request, 'auctions/categories.html', context)

def category_detail(request, category):
    active_listings = Listing.objects.filter(category=category, completed=False)
    context = {
        'category': category,
        'listing' : active_listings,
    }
    return render(request, 'auctions/category_details.html', context)