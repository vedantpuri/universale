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
from django.forms.widgets import Input, TextInput


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
    first_name = forms.CharField(max_length=100, help_text='Your first name', widget=forms.TextInput
      (attrs={'class' : 'form-control'}))
    last_name = forms.CharField(max_length=100, help_text='last_name', widget=forms.TextInput
      (attrs={'class' : 'form-control'}))
    bio = forms.CharField(max_length=500, help_text='Enter your bio', widget=forms.TextInput
      (attrs={'class' : 'form-control'}))
    College = (
        ('u', 'UMass Amherst'),
        ('a', 'Amherst College'),
        ('s', 'Smith College'),
        ('m', 'Mount Holyoke College'),
        ('h', 'Hamshire College'),
    )
    college = forms.ChoiceField(choices=College,widget=forms.Select(attrs={'class' : 'form-control'}))
    image = forms.FileField(required=False, widget=forms.FileInput(attrs={'class' : 'form-control'}))
    username = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter your email'}))
    password1=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2=forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-type your password'}))

    class Meta:
        model = DjangoUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'bio', 'college', 'image',)#('username', 'password1', 'password2',)
        # widgets = {
        # 'username': forms.EmailInput(attrs={'class' : 'form-control'}),
        # 'password1': forms.TextInput(attrs={'class' : 'form-control'}),
        # 'password2': forms.TextInput(attrs={'class' : 'form-control'}),
        # }  


# class YourRegistrationForm(RegistrationForm):
#     first_name = forms.CharField(max_length=100)

#     def save(self, profile_callback=None):
#         new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
#         password=self.cleaned_data['password1'],
#         email = self.cleaned_data['email'])
#         new_profile = User(user=new_user, first_name=self.cleaned_data['first_name'])
#         new_profile.save()
#         return new_user
