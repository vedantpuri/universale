from django.shortcuts import render
from ffs.models import Product
from ffs.models import User
# Create your views here.
def product_list_view(request):
	queryset = Product.objects.filter(title__icontains='textbook')

	context = {
		'object_list':queryset
	}

	return render(request, 'details.html', context)

def user_view(request):
	user = User.objects.get(email='samuelljackson@umass.edu')
	fname = user.first_name
	lname = user.last_name
	# college = user.get_College()
	bio = user.bio
	image = user.image
	email = user.email
	context = {
		'fname': fname,
		'lname': lname,
		# 'college': college,
		# 'bio': bio
		'image' : image,
		'email' : email
	}
	return render(request, 'user.html', context)
