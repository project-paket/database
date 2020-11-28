from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from lab5_3.apps import DB


def show_tables(request):
    if DB.a.login:
        return render(request, 'root/main_root.html', {'tables': DB.a.get_tables()})
    DB.scripts = 'wrong password or login'
    return HttpResponseRedirect(reverse('main_form:index'))


def show_components(request):
    if DB.a.login and DB.a.lvl == 3 or DB.a.login and DB.a.lvl == 2 or DB.a.login and DB.a.lvl == 0:
        save = DB.scripts
        DB.scripts = None
        link = 'http://127.0.0.1:8000/root/enter_components/'
        link2 = 'http://127.0.0.1:8000/root/enter_components_s/'
        return render(request, 'root/show_table.html',
                      {'tittles': DB.a.show_components()[0], 'strings': DB.a.show_components()[1:], 'link': link,
                       'link2': link2, 'last': DB.a.show_components()[-1], 'scripts': save})
    DB.scripts = 'wrong password or login'
    return HttpResponseRedirect(reverse('main_form:index'))

def show_table_old(request):
    if DB.a.login and DB.a.lvl == 3 or DB.a.login and DB.a.lvl == 2 or DB.a.login and DB.a.lvl == 0:
        save = DB.scripts
        DB.scripts = None
        if 'table' in request.POST:
            DB.link = request.POST['table']
        if 'link' in request.POST:
            link = request.POST['link']
        else:
            link = DB.link
            DB.link = None
        DB.link = link
        if '_apply' in request.POST:
            if request.POST['operation'] == 'INSERT':
                DB.a.del_string(request.POST['id'], request.POST['table'])
            elif request.POST['operation'] == 'DELETE':
                mass = []
                m = DB.a.output_titles(request.POST['table'])
                for i in request.POST:
                    if i in m:
                        mass.append(request.POST[i])
                DB.a.insert(mass, request.POST['table'])
            elif request.POST['operation'] == 'UPDATE':
                mass = []
                m = DB.a.output_titles(request.POST['table'])
                for i in request.POST:
                    if i in m:
                        mass.append(request.POST[i])
                mass.append(request.POST['id'])
                DB.a.update(mass, request.POST['table'])
            return HttpResponseRedirect(reverse('root:show_table'))
        else:
            return render(request, 'root/backups.html',
                          {'tables': DB.a.get_tables(),
                           'table': link,
                           'titles': DB.a.output_titles('{}_old'.format(link)),
                           'strings': DB.a.output_tables('{}_old'.format(link)), 'scripts': save})
    DB.scripts = 'wrong password or login'
    return HttpResponseRedirect(reverse('main_form:index'))

def show_dumps(request):
    if DB.a.login and DB.a.lvl == 3 or DB.a.login and DB.a.lvl == 2 or DB.a.login and DB.a.lvl == 0:
        save = DB.scripts
        DB.scripts = None
        if 'table' in request.POST:
            DB.link = request.POST['table']
        if 'link' in request.POST:
            link = request.POST['link']
        else:
            link = DB.link
            DB.link = None
        DB.link = link
        if '_create_dumps' in request.POST:
            DB.crt_brack_on_start()
            return HttpResponseRedirect(reverse('root:show_dumps'))
        elif '_restore' in request.POST:
            del DB.a
            DB.restore_db(request.POST['dump'])
            DB.a = DB.DB('admin', 'admin')
            return HttpResponseRedirect(reverse('root:show_dumps'))
        else:
            return render(request, 'root/dumps.html',
                          {'strings': DB.watch_dir()})
    DB.scripts = 'wrong password or login'
    return HttpResponseRedirect(reverse('main_form:index'))

def show_table(request):
    if DB.a.login:
        save = DB.scripts
        DB.scripts = None
        if 'table' in request.POST:
            DB.link = request.POST['table']
        if DB.a.lvl == 3 or DB.a.lvl == 0 or DB.a.lvl == 2:
            if '_del' in request.POST:
                DB.a.del_string(request.POST['id_old'], request.POST['table'])
            elif '_edit' in request.POST:
                mass = []
                m = DB.a.output_titles(DB.link)
                for i in request.POST:
                    if i in m:
                        mass.append(request.POST[i])
                mass.append(request.POST['id_old'])
                try:
                    DB.a.update(mass, DB.link)
                except:
                    DB.a.rollback()
                    DB.scripts = 'incorrect input'
            elif '_add' in request.POST:
                try:
                    mass = []
                    m = DB.a.output_titles(DB.link)
                    for i in request.POST:
                        if i in m:
                            mass.append(request.POST[i])
                    DB.a.insert(mass, DB.link)
                except Exception as e:
                    print(e)
                    DB.a.rollback()
                    DB.scripts = 'incorrect input'

        if 'link' in request.POST:
            link = request.POST['link']
        else:
            link = DB.link
            DB.link = None
        if DB.a.output_tables(link):
            last = DB.a.output_tables(link)[-1]
        else:
            last = None
        if '_search' in request.POST:
            DB.link = link
            mass = []
            m = DB.a.output_titles(DB.link)
            for i in request.POST:
                if i in m:
                    mass.append(request.POST[i])

            return render(request, 'root/show_table.html', {
                'tables': DB.a.get_tables(),
                'table': link,
                'titles': DB.a.output_titles(link),
                'strings': DB.a.search_component(request.POST['table'], mass),
                'last': last,
                'scripts': save
            })
        else:
            DB.link = link
            return render(request, 'root/show_table.html',
                          {'tables': DB.a.get_tables(),
                           'table': link,
                           'titles': DB.a.output_titles(link),
                           'last': last,
                           'strings': DB.a.output_tables(link), 'scripts': save})
    DB.scripts = 'wrong password or login'
    return HttpResponseRedirect(reverse('main_form:index'))

def enter_table(request):
    if DB.a.login and DB.a.lvl == 3 or DB.a.login and DB.a.lvl == 2 or DB.a.login and DB.a.lvl == 0:

        return HttpResponseRedirect(reverse('root:show_table'))

    DB.scripts = 'wrong password or login'
    return HttpResponseRedirect(reverse('main_form:index'))

def back_num(request):
    if DB.a.login and DB.a.lvl == 3 or DB.a.login and DB.a.lvl == 2 or DB.a.login and DB.a.lvl == 0:
        DB.a.back_num(request.POST['num'], request.POST['table'])
        return HttpResponseRedirect(reverse('root:show_table'))

    DB.scripts = 'wrong password or login'
    return HttpResponseRedirect(reverse('main_form:index'))

