from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from web.models import *
from .database_lib import *
from .send_msg import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
# Create your views here.

def index(request):
    if request.flavour == 'mobile':
        return redirect(m_index)
    return render(request, "web/index.html", {'info': get_index_info()})


def detail(request):
    if request.flavour == 'mobile':
        return HttpResponseRedirect('/m/detail?id=%s' % request.GET.get('id'))
        # return redirect(m_detail)
    teacher = get_teacher_of(request.GET.get('id'))
    # print(type())
    # teacher.settime_slot(['周六下午'])
    # teacher.save()
    return render(request, "web/detail.html", {'teacher': teacher,
                            'slots': teacher.get_time_slot()})


def teachers(request):
    if request.flavour == 'mobile':
        return redirect(m_teachers)
    ts = teacher.objects.all()
    info = [{'ts': t, 'slots': t.get_time_slot()} for t in ts]
    gender = request.GET.get('gender')
    subject = request.GET.get('subject')

    gender = None if gender == 'None' else gender
    subject = None if subject == 'None' else subject

    if gender:
        g = 0 if gender=='male' else 1
        info = [x for x in info if (lambda y: y['ts'].gender == g)(x)]

    if subject:
        info = [x for x in info if (lambda y: y['ts'].subject.find(subject) != -1)(x)]


    paginator = Paginator(info, 10)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        contacts = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "web/teachers.html", {'info': contacts,
                                'gender': gender,
                                'subject': subject,
                                'now_page': page,
                                'page_nums': range(1, paginator.num_pages+1) })


def about(request):
    if request.flavour == 'mobile':
        return redirect(m_about)
    return render(request, "web/about.html", {'ab': about_us.objects.all()[0]})


def activity(request):
    if request.flavour == 'mobile':
        return redirect(m_activity)
    return render(request, "web/activity.html")


@login_required()
def teacher_slot(request):
    ts = teacher.objects.all()
    info = [{'ts': t, 'slots': t.get_time_slot()} for t in ts]
    return render(request, "web/teacher_slot.html", {'info': info})


@login_required()
def detail_slot(request, mothods=['GET', 'POST']):
    if request.method == 'POST':
        print(request.POST.get('id'))
        te = get_teacher_of(request.POST.get('id'))
        te.set_time_slot(json.loads(request.POST.get('slots')))
        te.save()
        return JsonResponse({'code':0})
    teacher = get_teacher_of(request.GET.get('id'))
    return render(request, "web/detail_slot.html", {'t': teacher,
                            'slots': teacher.get_time_slot()})


@login_required()
def rsv_manage(request):
    rsvs = reservation.objects.all()
    info = [{'rsv': t, 'slots': t.get_time_slot()} for t in rsvs]
    return render(request, "web/rsv_manage.html", {'info': info})



def new_reservation(request, method=['POST']):
    # check code
    phone_num = request.POST.get("phone_num")
    print(request.session.get(phone_num), request.POST.get("code"))
    if request.session.get(phone_num) != request.POST.get("code"):
        return JsonResponse({
                'code': 1,
                'msgs': ['验证码错误']
            })

    name = request.POST.get("name")
    address = request.POST.get("address")
    teacher = get_teacher_of(request.POST.get("id"))
    time_slot = json.loads(request.POST.get("time_slot"))

    rsv = reservation(name=name, phone_num=phone_num, address=address, teacher=teacher)
    rsv.set_time_slot(time_slot)

    rsv.save()

    request.session.pop(phone_num);
    return JsonResponse({'code': 0})


from datetime import datetime
import random
def send_code(request, method=['POST']):
    if request.session.get("last-time"):
        delta = datetime.now() - datetime.strptime(request.session["last-time"],
                                    "%Y %m %d %H %M %S")
        if delta.seconds < 120:
            return JsonResponse({"code": 202, "delta": delta.seconds})
    # do sending things
    phone_num = request.POST.get("phone_num")
    c = str(random.randint(100000, 999999))
    request.session[phone_num] = c
    code, rsp = send_msg(c, phone_num)
    print(c)

    request.session["last-time"] = datetime.now().strftime("%Y %m %d %H %M %S")
    return JsonResponse({"code": code, "ret": rsp})


#### mobile pages
def m_index(request):
    if request.flavour == 'full':
        return redirect(index)
    return render(request, "web/m_index.html", {'info': get_index_info()})


def m_detail(request):
    if request.flavour == 'full':
        return HttpResponseRedirect('/detail?id=%s' % request.GET.get('id'))
        # return redirect('/detail')
    teacher = get_teacher_of(request.GET.get('id'))
    # print(type())
    # teacher.settime_slot(['周六下午'])
    # teacher.save()
    return render(request, "web/m_detail.html", {'teacher': teacher,
                            'slots': teacher.get_time_slot()})


def m_teachers(request):
    if request.flavour == 'full':
        return redirect(teacher)
    ts = teacher.objects.all()
    info = [{'ts': t, 'slots': t.get_time_slot()} for t in ts]
    gender = request.GET.get('gender')
    subject = request.GET.get('subject')

    gender = None if gender == 'None' else gender
    subject = None if subject == 'None' else subject

    if gender:
        g = 0 if gender=='male' else 1
        info = [x for x in info if (lambda y: y['ts'].gender == g)(x)]

    if subject:
        info = [x for x in info if (lambda y: y['ts'].subject.find(subject) != -1)(x)]


    paginator = Paginator(info, 10)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        contacts = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "web/m_teachers.html", {'info': contacts,
                                'gender': gender,
                                'subject': subject,
                                'now_page': page,
                                'page_nums': range(1, paginator.num_pages+1) })


def m_about(request):
    if request.flavour == 'full':
        return redirect(about)
    return render(request, "web/m_about.html", {'ab': about_us.objects.all()[0]})


def m_activity(request):
    if request.flavour == 'full':
        return redirect(activity)
    return render(request, "web/m_activity.html")




def change_rsv_status(request, method=['POST']):
    _id = request.POST.get('id')
    status = request.POST.get('status')
    set_rsv_status(_id, status)
    return JsonResponse({'code': 0})