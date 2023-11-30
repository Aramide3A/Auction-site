from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    categories = [
        ("Entertainment", 'Entertainment'),
        ("Tech", 'Tech'),
        ("Fashion", 'Fashion'),
    ]
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    title = models.CharField(max_length=69)
    description= models.TextField()
    starting_bid = models.IntegerField()
    current_bid = models.IntegerField(null=True, blank= True)
    winner = models.ForeignKey(User, on_delete= models.CASCADE, blank=True, null=True, related_name='auction_winner')
    image = models.URLField(null=True, blank= True)
    category = models.CharField(choices=categories, max_length=69)
    time_created= models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default= False)

    def __str__(self) :
        return self.title

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    listing = models.ManyToManyField(Listing, related_name='listing')

    def __str__(self) :
        return f"{self.user}'s watchlist"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,related_name='user_bid')
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE)
    amount = models.IntegerField()
    time_created= models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"{self.user}'s bid for {self.listing}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name='comment')
    text = models.TextField()
    time_created= models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"{self.user}'s comment for {self.listing}"
