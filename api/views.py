from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse

from server.const import BOT_NAME
from server.const import BASH_BEGINING
from server.const import BASH_SPLITER
from server.const import HOST_DNS

from .models import TelegramUsers
from .models import Scripts
from .models import Templates


class Main(View):
    def get(self, request):
        bot_name = BOT_NAME
        session_id = request.session["session_id"]
        auth = request.session["auth"]
        return render(request, 'main.html', {"bot_name":bot_name, "session_id":session_id, "auth":auth})
    
class Login(View):
    def get(self, request):
        session_id = request.session["session_id"]
        telegram_login_url = f"https://t.me/{BOT_NAME}?start={session_id}"
        return redirect(telegram_login_url)

class AuthCheck(View):
    def get(self, request):
        session_id = request.GET.get('session_id')
        if TelegramUsers.objects.filter(session_id=session_id).exists():
            return JsonResponse({'result': True})
        else:
            return JsonResponse({'result': False})

class Logout(View):
    def get(self, request):
        session_id = request.session["session_id"]
        if TelegramUsers.objects.filter(session_id=session_id).exists():
            user = TelegramUsers.objects.get(session_id=session_id)
            user.session_id = "None"
            user.save()

        request.session["session_id"]=None
        request.session["auth"]=None
        request.session["name"]=None
        return redirect("/")
    
# script

class ScriptCreate(View):
    def get(self, request):
        return render(request, 'script/script_create.html')
    
    def post(self, request):
        session_id = request.session["session_id"]        
        user = TelegramUsers.objects.get(session_id=session_id)
        tg_id = user.tg_id
        name = request.POST["name"]
        text = request.POST["text"]
        script = Scripts.objects.create(name=name, author=tg_id, text=text)
        script.save()
        return redirect("/script_list/")
    
class ScriptList(View):
    def get(self, request):
        session_id = request.session["session_id"]        
        user = TelegramUsers.objects.get(session_id=session_id)
        tg_id = user.tg_id
        script_list = Scripts.objects.filter(author=tg_id)
        return render(request, 'script/script_list.html', {"script_list":script_list})

class ScriptId(View):
    def get(self, request, script_id):
        if not Scripts.objects.filter(id=script_id).exists():
            info = "Скрипт не найден, попробуйте еще раз"
            return render(request, 'info.html', {"info":info})
        
        script = Scripts.objects.get(id=script_id)
        return render(request, 'script/script_id.html', {'script':script, 'host_dns':HOST_DNS})

class ScriptDelete(View):   # надо дописать - запрет удаления скриптов которые используются в темплейтах
    def post(self, request, script_id):
        if not Scripts.objects.filter(id=script_id).exists():
            info = "Скрипт не найден, попробуйте еще раз"
            return render(request, 'info.html', {"info":info})
        
        session_id = request.session["session_id"]  
        user = TelegramUsers.objects.get(session_id=session_id)
        script = Scripts.objects.get(id=script_id)

        if user.tg_id != script.author:
            info = "У вас нет прав на удаление"
            return render(request, 'info.html', {"info":info})
        
        script.delete()
        return redirect("/script_list/")
    
class ScriptRaw(View):
    def get(self, request, script_id):
        if not Scripts.objects.filter(id=script_id).exists():
            info = "Скрипт не найден, попробуйте еще раз"
            return render(request, 'info.html', {"info":info})
        
        script = Scripts.objects.get(id=script_id)
        raw_script_name = f"\r\necho \"complited {script.name} \" "
        raw = BASH_BEGINING + script.text + BASH_SPLITER + raw_script_name + BASH_SPLITER

        response = HttpResponse(raw.encode('utf-8'), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=script_raw.sh'
        return response
    
# template

class TemplateCreate(View):
    def get(self, request):    # form
        return
    
    def post(self, request):   # save
        return
    
class TemplateList(View):
    def get(self, request):
        return

class TemplateId(View):
    def get(self, request, template_id):    # inspekt
        return
    
    def post(self, request, template_id):   # edit
        return 
    
class TemplateDelete(View):
    def post(self, request, template_id):
        return
    
class TemplateRaw(View):
    def get(self, request):
        return
    


# TESTING
import json
from django.views.decorators.csrf import csrf_exempt

def order_page(request):
    menu_items = ["Pizza", "Burger", "Pasta", "Salad", "Sushi"]
    return render(request, 'testing/order_page.html', {'menu_items': menu_items})

@csrf_exempt
def submit_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order = data.get('order', [])
        comment = data.get('comment', '')

        print("Order received:", comment)
        print("Order received:", order)  # For now, just print the order
        return JsonResponse({"status": "success", "order": order})
    return JsonResponse({"status": "error"}, status=400)