from .models import *
from django.forms import ModelForm

class Listing_form(ModelForm):
    class Meta:
        model = Listing
        exclude = ['user','time_created','current_bid', 'winner', 'completed']

class Bid_Form(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text':'Comment',
        }