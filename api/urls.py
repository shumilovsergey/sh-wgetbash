from django.urls import path

from .views import Main
from .views import Login
from .views import Logout
from .views import AuthCheck
from .views import Info

from .views import ScriptList
from .views import ScriptId
from .views import ScriptDelete
from .views import ScriptCreate
from .views import ScriptRaw

from .views import TemplateList
from .views import TemplateId
from .views import TemplateDelete
from .views import TemplateCreate
from .views import TemplateRaw

# testing 
from . import views

app_name = 'api'
urlpatterns = [
    # core
    path('', Main.as_view(), name='main'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('auth_check/', AuthCheck.as_view(), name='auth_check'),
    path('info/', Info.as_view(), name='info'),
    # script
    path('script_list/', ScriptList.as_view(), name='script_list'),
    path('script_id/<int:script_id>/', ScriptId.as_view(), name='script_id'),
    path('script_delete/<int:script_id>/', ScriptDelete.as_view(), name='script_delete'),     # script_delete warning
    path('script_create/', ScriptCreate.as_view(), name='script_create'),
    path('script_raw/<int:script_id>/', ScriptRaw.as_view(), name='script_raw'),
    # template
    path('template_list/', TemplateList.as_view(), name='template_lis'),
    path('template_id/<int:template_id>/', TemplateId.as_view(), name='template_id'),
    path('template_edit/<int:template_id>/', TemplateId.as_view(), name='template_edit'),
    path('template_delete/<int:template_id>/', TemplateDelete.as_view(), name='template_delete'),
    path('template_create/', TemplateCreate.as_view(), name='template_create'),
    path('template_raw/<int:template_id>/', TemplateRaw.as_view(), name='template_raw'),
    # testing
]