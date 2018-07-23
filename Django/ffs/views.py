from django.shortcuts import render
from ffs.models import Product
from ffs.models import Student
from ffs.models import Flag
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

def landing_view(request):
 	return render(request, 'landing-page.html', context={})

def search_view(request):
	query = request.GET.get("q")
	queryset = Product.objects.filter(title__icontains=query)
	context = { 'results': queryset, 'entered_text': query }
	return render(request, 'search_result_page.html', context)

@login_required(login_url="/accounts/login/")
def flagged_view(request):
	items = Flag.objects.filter(user=request.user.student)
	lst = []
	for item in items:
		lst += [j for j in item.products.all()]
	return render(request, 'flagged_items_page.html', { 'flagged_items' : lst })

@csrf_exempt
@login_required(login_url="/accounts/login/")
def add_to_flagged(request):
	if request.method == 'POST':
		print(request.POST)
		current_user = request.user.student
		id = request.POST.get("product_id")
		prod_obj = Product.objects.get(pk=id)
		qs = Flag.objects.filter(user=current_user, products=prod_obj)
		# Check to prevent user to flag own item and prevent user to flag same item multiple times
		if not qs.exists() and prod_obj.owner != current_user:
			prod_obj.flag_count += 1
			prod_obj.save()
			flag_obj = Flag.objects.create(user=current_user)
			flag_obj.products.add(prod_obj)
	return redirect("/flagged/")


@csrf_exempt
@login_required(login_url="/accounts/login/")
def remove_from_flagged(request):
	flagged = Flag.objects.all()
	if request.method == 'POST':
		current_user = request.user.student
		id = request.POST.get("product_id")
		prod_obj = Product.objects.get(pk=id)
		flag_obj = Flag.objects.get(user=current_user, products=prod_obj)
		flag_obj.delete()
		if prod_obj.flag_count > 0:
			prod_obj.flag_count -= 1
			prod_obj.save()
	return redirect("/flagged/")

@login_required(login_url="/accounts/login/")
def user_view(request):
	return render(request, 'user.html', {'current_user' : request.user.student})

@login_required(login_url="/accounts/login/")
def view_alt_user(request):
	if request.method == 'GET':
		user_id = request.GET['user_obj']
		alt_user = Student.objects.get(id=user_id)
	return render(request, 'alt_user.html', {'alt_user': alt_user})

@csrf_exempt
@login_required(login_url="/accounts/login/")
def remove_from_user(request):
	if request.method == 'POST':
		id = request.POST.get("product_id")
		prod_inst = Product.objects.get(pk=id)
		prod_inst.delete()
	return redirect("/user/")

from .forms import UploadProductForm
@login_required(login_url="/accounts/login/")
def upload_view(request):
	if request.method == "POST":
		form = UploadProductForm(request.POST, request.FILES)
		if form.is_valid():
			product_instance = form.save(commit=False)
			product_owner = request.user.student
			product_instance.owner = product_owner
			product_instance.save()
			return HttpResponseRedirect("../user/?success")
	else:
		form = UploadProductForm()
	return render(request, 'upload-page.html', {'form': form})

from .forms import EditProfileForm
@login_required(login_url="/accounts/login/")
def edit_profile_view(request):
	logged_in_user = request.user.student
	college = logged_in_user.get_college_display()
	form = EditProfileForm(instance=logged_in_user)
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=logged_in_user)
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
        	student = Student(django_user=user,
        		first_name=form.cleaned_data.get('first_name'),
        		last_name=form.cleaned_data.get('last_name'),
        		bio=form.cleaned_data.get('bio'),
        		college = form.cleaned_data.get('college'),
        		email = form.cleaned_data.get('username'),
        		star_count = 0,
        		image = request.FILES.get('image')
        		)
        	student.save()
        	login(request, user)
        	return render(request, 'landing-page.html', context={})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
