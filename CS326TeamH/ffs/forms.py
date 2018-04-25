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
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.forms import UserCreationForm
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

    class Meta:
        model = User
        fields = ['image', 'first_name', 'last_name', 'bio', 'college', 'email']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Your first name')
    last_name = forms.CharField(max_length=100, help_text='last_name')
    bio = forms.CharField(max_length=500, help_text='Enter your bio')
    College = (
        ('u', 'Umass Amherst'),
        ('a', 'Amherst College'),
        ('s', 'Smith College'),
        ('m', 'Mount Holyoke College'),
        ('h', 'Hamshire College'),
    )
    college = forms.ChoiceField(choices=College)
    image = forms.ImageField(required=False)


    class Meta:
        model = DjangoUser
        fields = ('username', 'password1', 'password2',)


# class YourRegistrationForm(RegistrationForm):
#     first_name = forms.CharField(max_length=100)

#     def save(self, profile_callback=None):
#         new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
#         password=self.cleaned_data['password1'],
#         email = self.cleaned_data['email'])
#         new_profile = User(user=new_user, first_name=self.cleaned_data['first_name'])
#         new_profile.save()
#         return new_user
