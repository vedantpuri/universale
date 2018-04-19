from django.shortcuts import render
from ffs.models import Product
from ffs.models import User
from ffs.models import Flag
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

# Create your views here.
def product_list_view(request):
	queryset = Product.objects.filter(title__icontains='textbook')

	context = {
		'object_list':queryset
	}

	return render(request, 'details.html', context)

@login_required(login_url="/accounts/login/")
def user_view(request):
	print("Current User", request.user.user)
	user = request.user.user#User.objects.get(email='samuelljackson@umass.edu')
	fname = user.first_name
	lname = user.last_name

	bio = user.bio
	image = user.image
	email = user.email
	products = user.product_set.all()
	college = user.get_college_display()
	count = products.count()
	star = user.star_count
	flagged = Flag.objects.all()
	lst = []

	for i in products:
		ctr = 0
		title = i.title
		for j in flagged:
			tmp = j.products.all()
			if len(tmp)>0 and tmp[0].title == title:
				ctr += 1
		lst.append(ctr)
	context = {
		'fname': fname,
		'lname': lname,
		'college': college,
		'bio': bio,
		'image' : image,
		'email' : email,
		'products': zip(products, lst),
		'count': count,
		'star': star
	}
	return render(request, 'user.html', context)

def search_view(request):
	query = request.GET.get("q")
	queryset = Product.objects.filter(title__icontains=query)
	flagged = Flag.objects.all()
	lst = []

	for i in queryset:
		ctr = 0
		title = i.title
		for j in flagged:
			tmp = j.products.all()
			if len(tmp)>0 and tmp[0].title == title:
				ctr += 1
		lst.append(ctr)

	context = {
		'object_list' : zip(queryset, lst),
		'check': queryset,
		'entered_text': query
	}

	return render(request, 'search_result_page.html', context)

@login_required(login_url="/accounts/login/")
def flagged_view(request):
	current_user = request.user.user

	flagged = Flag.objects.all()
	lst = []
	ctr_lst = []
	for i in flagged:
		if i.user.email == current_user.email:
			lst += [j for j in i.products.all()]
	for i in lst:
		ctr = 0
		title = i.title
		for j in flagged:
			tmp = j.products.all()
			if len(tmp)>0 and tmp[0].title == title:
				ctr += 1
		ctr_lst.append(ctr)

	context = {
			'object_list' : zip(lst, ctr_lst)
			}
	return render(request, 'flagged_items_page.html', context)

@csrf_exempt
@login_required(login_url="/accounts/login/")
def add_to_flagged(request):

	if request.method == 'POST':
		print(request.POST)
		current_user = request.user.user
		flag_obj = Flag.objects.create(user=current_user)
		prod_obj = Product.objects.filter(title__icontains=request.POST.get("product_title", "")).first()
		flag_obj.products.add(prod_obj)

	return redirect("/flagged/")

@csrf_exempt
@login_required(login_url="/accounts/login/")
def remove_from_flagged(request):
	flagged = Flag.objects.all()


	if request.method == 'POST':
		current_user = request.user.user
		for i in flagged:
			if i.user.email == current_user.email:
				if i.products.first() == Product.objects.filter(title__icontains=request.POST.get("product_title", "")).first():
					i.delete()
	return redirect("/flagged/")



def landing_view(request):
 	return render(request, 'landing-page.html', context={})

from .forms import UploadProductForm
@login_required(login_url="/accounts/login/")
def upload_view(request):
	if request.method == "POST":
		form = UploadProductForm(request.POST, request.FILES)
		if form.is_valid():
			product_instance = form.save(commit=False)
			# replace this line with logged in user
			product_owner = request.user.user#User.objects.get(email='samuelljackson@umass.edu')
			product_instance.owner = product_owner
			print(product_instance.description)
			product_instance.save()
			return HttpResponseRedirect("../user/?success")

			# redirect link here
	else:
		form = UploadProductForm()

	return render(request, 'upload-page.html', {'form': form})

from .forms import EditProfileForm
@login_required(login_url="/accounts/login/")
def edit_profile_view(request):
	# form = EditProfileForm(request.POST, request.FILES)

	user = request.user.user#User.objects.get(email='samuelljackson@umass.edu')
	college = user.get_college_display()
	form = EditProfileForm(instance=user)
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			# redirect link here
	return render(request, 'user_edit.html', {'form': form, 'user': user, 'user_college': college})
