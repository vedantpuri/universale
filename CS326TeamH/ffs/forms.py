from django import forms
from django.core.exceptions import ValidationError

class UploadProductForm(forms.Form):
    item_name = forms.CharField(label='Item Name', max_length=100, required=True)
    item_description = forms.CharField(widget=forms.Textarea, min_length=10)
    marked_price = forms.IntegerField(min_value=0, required=True)
