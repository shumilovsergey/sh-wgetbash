from django.urls import path

from .views import Main
from .views import Login
from .views import Logout
from .views import AuthCheck

from .views import ScriptList
from .views import ScriptId
from .views import ScriptDelete
from .views import ScriptCreate
from .views import ScriptRaw

app_name = 'api'
urlpatterns = [
    # core
    path('', Main.as_view(), name='main'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('auth_check/', AuthCheck.as_view(), name='auth_check'),
    # script
    path('script_list/', ScriptList.as_view(), name='script_list'),
    path('script_id/<int:script_id>/', ScriptId.as_view(), name='script_id'),
    path('script_delete/<int:script_id>/', ScriptDelete.as_view(), name='script_delete'),     # script_delete (no delete script in template)
    path('script_create/', ScriptCreate.as_view(), name='script_create'),
    path('script_raw/<int:script_id>/', ScriptRaw.as_view(), name='script_raw'),
    # template

    # template_list
    # template_id
    # template_delete
    # template_create
    # template_edit
    # template_raw

]