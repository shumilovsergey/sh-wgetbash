from django.urls import path
from .views import Main
from .views import Login
from .views import Logout
from .views import AuthCheck


app_name = 'api'
urlpatterns = [
    # core
    path('', Main.as_view(), name='main'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('auth_check/', AuthCheck.as_view(), name='auth_check')

    # script_list
    # script_id
    # script_delete (no delete script in template)
    # script_create
    # script_raw

    # template_list
    # template_id
    # template_delete
    # template_create
    # template_edit
    # template_raw

]