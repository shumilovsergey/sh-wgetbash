from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from server.const import BOT_NAME
from server.const import BASH_BEGINING
from server.const import BASH_SPLITER
from server.const import HOST_DNS

from .models import TelegramUsers
from .models import Scripts
from .models import Templates
from .models import MainPage


class Main(View):
    def get(self, request):
        bot_name = BOT_NAME
        session_id = request.session["session_id"]
        auth = request.session["auth"]
        data = MainPage.objects.all()
        data = data[0]
        
        return render(request, 'main.html', {"bot_name":bot_name, "session_id":session_id, "auth":auth, "data":data})
    
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

        request.session["session_id"]="logout"
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
        return render(request, 'script/script_list.html', {"script_list":script_list, 'host_dns':HOST_DNS})

class ScriptId(View):
    def get(self, request, script_id):
        if not Scripts.objects.filter(id=script_id).exists():
            info = "Скрипт не найден, попробуйте еще раз"
            return render(request, 'info.html', {"info":info})
        
        script = Scripts.objects.get(id=script_id)
        return render(request, 'script/script_id.html', {'script':script, 'host_dns':HOST_DNS})
    
    def post(self, request, script_id):
        if not Scripts.objects.filter(id=script_id).exists():
            info = "Скрипт не найден, попробуйте еще раз"
            return render(request, 'info.html', {"info":info})
        
        script = Scripts.objects.get(id=script_id)   
        session_id = request.session["session_id"]  
        user = TelegramUsers.objects.get(session_id=session_id)

        if user.tg_id != script.author:
            info = "У вас нет прав на запись"
            return render(request, 'info.html', {"info":info})

        script.name = request.POST["name"]
        script.text = request.POST["text"]
        script.save()
        return redirect("/script_list/")


class ScriptDelete(View):   # дописать предупреждение о том, что скрипт учавствует в темплейте
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
        raw_script_name = f"\necho \"complited {script.name} \" "
        raw = BASH_BEGINING + "\n" + script.text + BASH_SPLITER + raw_script_name + BASH_SPLITER

        response = HttpResponse(raw.encode('utf-8'), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=script_raw.sh'
        return response
    
# template

class TemplateCreate(View):
    def get(self, request):    # form
        session_id = request.session["session_id"]        
        user = TelegramUsers.objects.get(session_id=session_id)
        tg_id = user.tg_id
        script_list = Scripts.objects.filter(author=tg_id)
        return render(request, 'template/template_create.html', {'script_list': script_list})
    
    def post(self, request):   # save
        data = json.loads(request.body)
        script_list_id = data.get('script_list')
        template_name = data.get('template_name')

        session_id = request.session["session_id"]   
        user = TelegramUsers.objects.get(session_id=session_id) 
        template = Templates.objects.create(name=template_name, author=user)

        for script_id in script_list_id:
            if Scripts.objects.filter(id=script_id).exists():
                script = Scripts.objects.get(id=script_id)
                template.scripts.add(script)
        template.save()
        return JsonResponse({"status": "success"})

    
class TemplateList(View):
    def get(self, request):
        session_id = request.session["session_id"]        
        user = TelegramUsers.objects.get(session_id=session_id)
        template_list = Templates.objects.filter(author=user)
        template_list_clean = []

        for template in template_list:
            if template.scripts.count() < 1:
                template.delete()
            else:
                template_list_clean.append(template)
        return render(request, 'template/template_list.html', {"template_list":template_list_clean, "host_dns":HOST_DNS})

class TemplateId(View):
    def get(self, request, template_id):    # inspekt
        if not Templates.objects.filter(id=template_id).exists():
            info = "Шаблон не найден, попробуйте еще раз"
            return render(request, "info.html", {"info":info})
        
        template = Templates.objects.get(id=template_id)
        return render(request, 'template/template_id.html', {"template":template, "host_dns":HOST_DNS})
    
class TemplateDelete(View):
    def post(self, request, template_id):
        if not Templates.objects.filter(id=template_id).exists():
            info = "Шаблон не найден, попробуйте еще раз"
            return render(request, 'info.html', {"info":info})
        
        session_id = request.session["session_id"]  
        user = TelegramUsers.objects.get(session_id=session_id)
        template = Templates.objects.get(id=template_id)

        if user != template.author:
            info = "У вас нет прав на удаление"
            return render(request, 'info.html', {"info":info})
        
        template.delete()
        return redirect("/template_list/")
    
class TemplateRaw(View):
    def get(self, request, template_id):
        if not Templates.objects.filter(id=template_id).exists():
            info = "Шаблон не найден, попробуйте еще раз"
            return render(request, 'info.html', {"info":info})
        
        template = Templates.objects.get(id=template_id) 
        template_raw = BASH_BEGINING

        for script in template.scripts.all():
            raw_script_name = f"\necho \"complited {script.name} \" "
            raw_script_text = "\n" + script.text + BASH_SPLITER + raw_script_name + BASH_SPLITER
            template_raw = template_raw + raw_script_text

        response = HttpResponse(template_raw.encode('utf-8'), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=template_raw.sh'
        return response
    
