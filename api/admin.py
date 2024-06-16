from django.contrib import admin
from .models import TelegramUsers
from .models import Scripts
from .models import Templates


admin.site.register(TelegramUsers)
admin.site.register(Scripts)
admin.site.register(Templates)
