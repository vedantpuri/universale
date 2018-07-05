from django.shortcuts import render
from ffs.models import Product
from ffs.models import User
from ffs.models import Flag
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate


def product_list_view(request):
	queryset = Product.objects.filter(title__icontains='textbook')

	context = {
		'object_list':queryset
	}

	return render(request, 'details.html', context)


@login_required(login_url="/accounts/login/")
def user_view(request):
	user = request.user.user
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
	query = request.GET.get("q")
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


@login_required(login_url="/accounts/login/")
def view_alt_user(request):

	if request.method == 'GET':
		print(request.GET)
		user_id = request.GET['user_obj']
		alt_user = User.objects.get(id=user_id)
		print(alt_user.first_name)

		fname = alt_user.first_name
		lname = alt_user.last_name
		flagged = Flag.objects.all()
		bio = alt_user.bio
		image = alt_user.image
		email = alt_user.email
		products = alt_user.product_set.all()
		college = alt_user.get_college_display()
		count = products.count()
		star = alt_user.star_count
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

	return render(request, 'alt_user.html', context)


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


@csrf_exempt
@login_required(login_url="/accounts/login/")
def remove_from_user(request):
	if request.method == 'POST':
		id = request.POST.get("product_id")
		prod_inst = Product.objects.get(pk=id)
		print(prod_inst)
		prod_inst.delete()
	return redirect("/user/")


def landing_view(request):
 	return render(request, 'landing-page.html', context={})


from .forms import UploadProductForm
@login_required(login_url="/accounts/login/")
def upload_view(request):
	if request.method == "POST":
		form = UploadProductForm(request.POST, request.FILES)
		if form.is_valid():
			product_instance = form.save(commit=False)
			product_owner = request.user.user
			product_instance.owner = product_owner
			product_instance.save()
			return HttpResponseRedirect("../user/?success")

			# redirect link here
	else:
		form = UploadProductForm()

	return render(request, 'upload-page.html', {'form': form})


from .forms import EditProfileForm
@login_required(login_url="/accounts/login/")
def edit_profile_view(request):
	user = request.user.user
	college = user.get_college_display()
	form = EditProfileForm(instance=user)
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
	return render(request, 'user_edit.html', {'form': form, 'user_college': college})


from .forms import SignUpForm
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
        	user = form.save()
        	username = form.cleaned_data.get('username')
        	password = form.cleaned_data.get('password1')
        	ffs_user = User(user=user,
        		first_name=form.cleaned_data.get('first_name'),
        		last_name=form.cleaned_data.get('last_name'),
        		bio=form.cleaned_data.get('bio'),
        		college = form.cleaned_data.get('college'),
        		email = form.cleaned_data.get('username'),
        		star_count = 0,
        		image = request.FILES.get('image')
        		)
        	ffs_user.save()
        	login(request, user)
        	return render(request, 'landing-page.html', context={})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
