from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from lab5_3.apps import DB

scripts = None

def index(request):
    if 'login' in request.POST and 'password' in request.POST:
        DB.a = DB.DB(request.POST['login'], request.POST['password'], )
        if DB.a.login:
            return HttpResponseRedirect(reverse('root:show_tables'))
        DB.scripts = 'wrong password or login'
        return HttpResponseRedirect(reverse('main_form:index'))
    return render(request, 'authentication_form/main_form.html', {'scripts': DB.scripts})