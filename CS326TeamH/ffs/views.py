from django.shortcuts import render
from ffs.models import Product
from ffs.models import User
from ffs.models import Flag
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
	products = user.product_set.all()
	college = user.get_college_display()
	count = products.count()
	star = user.star_count
	context = {
		'fname': fname,
		'lname': lname,
		'college': college,
		'bio': bio,
		'image' : image,
		'email' : email,
		'products': products,
		'count': count,
		'star': star
	}
	return render(request, 'user.html', context)

def search_view(request):
	queryset = Product.objects.filter(title__icontains='textbook')
	
	print(len(queryset))

	context = {
		'object_list' : queryset
	}

	return render(request, 'search_result_page.html', context)

def flagged_view(request):
	flagged = Flag.objects.all()
	lst = []
	for i in flagged:
		if i.user.email == 'sthapar@umass.edu':
			lst += [j for j in i.products.all()]
	context = {
			'object_list' : lst
			}


	return render(request, 'flagged_items_page.html', context)


	


