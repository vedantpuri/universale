from django.shortcuts import render
from ffs.models import Product
# Create your views here.
def product_list_view(request):
	queryset = Product.objects.filter(title__icontains='textbook')
	
	context = { 
		'object_list':queryset
	}

	return render(request, 'details.html', context)

