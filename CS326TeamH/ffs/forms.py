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
from django.core.exceptions import ValidationError

class UploadProductForm(ModelForm):
   title = forms.CharField(label='Item Name', max_length=100, required=True)
   description = forms.CharField(widget=forms.Textarea, min_length=10)
   price = forms.IntegerField(min_value=0, required=True)
<<<<<<< HEAD
   image = forms.ImageField(required=True)
=======
   # item_image = forms.FileField(required=True)
>>>>>>> 7a5481f86dbca9e2725db35964819fa7f17b0aa2
   class Meta:
       model = Product
       fields = ['title', 'description', 'price', 'image']
