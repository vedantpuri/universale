from django.urls import path
from . import views
from ffs.views import product_list_view
from ffs.views import user_view
from ffs.views import search_view
from ffs.views import flagged_view
from ffs.views import landing_view
from ffs.views import upload_view
from ffs.views import edit_profile_view
from ffs.views import add_to_flagged
from ffs.views import remove_from_flagged
from ffs.views import view_alt_user
from ffs.views import signup
from ffs.views import remove_from_user

urlpatterns = [
	path('user/', user_view, name='user'),
	path('search/', search_view, name='search'),
	path('flagged/', flagged_view, name='flag'),
	path('flagged/remove/', remove_from_flagged, name='flag_remove'),
	path('user/remove_product/', remove_from_user, name='user_prod_remove'),
	path('search/add/', add_to_flagged, name='search_add'),
	path('upload/', upload_view, name='upload'),
	path('edit_profile/', edit_profile_view, name="user_edit"),
	path('alt_user/', view_alt_user, name='alt_user'),
	path('', landing_view, name='home'),
	path('signup/', signup, name='signup'),

]
