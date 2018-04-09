# from django import forms
# from django.core.exceptions import ValidationError
#
# class UploadProductForm(forms.Form):
#     item_name = forms.CharField(label='Item Name', max_length=100, required=True)
#     item_description = forms.CharField(widget=forms.Textarea, min_length=10)
#     marked_price = forms.IntegerField(min_value=0, required=True)
#     item_image = forms.ImageField(required=True)

from django import forms
from django.forms import ModelForm
from ffs.models import Product
from ffs.models import User
from django.core.exceptions import ValidationError

class UploadProductForm(ModelForm):
   title = forms.CharField(label='Item Name', min_length=5, max_length=100, required=True, help_text='Should be more than 5 characters and less than 100 characters')
   description = forms.CharField(widget=forms.Textarea, min_length=10)
   price = forms.IntegerField(min_value=0, required=True)
   # image = forms.ImageField(required=True)
   class Meta:
       model = Product
       fields = ['title', 'description', 'price', 'image']

class EditProfileForm(ModelForm):
    #first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': User.first_name}))
    #last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': User.last_name}))
    #bio = forms.CharField(widget=forms.TextInput(attrs={'placeholder': User.bio}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': User.email}))
    #college = forms.CharField(widget=forms.TextInput(attrs={'placeholder': User.last_name}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'college', 'email', 'image']
