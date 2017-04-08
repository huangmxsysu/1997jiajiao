"""proj_1997 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from web import views as web_views

urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', web_views.index, name='index'),
    url(r'^detail$', web_views.detail, name='detail'),
    url(r'^activity$', web_views.activity, name='activity'),
    url(r'^teachers$', web_views.teachers, name='teachers'),
    url(r'^about$', web_views.about, name='about'),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^admin/r$', web_views.rsv_manage, name='rsv_manage'),
    url(r'^admin/r/status$', web_views.change_rsv_status, name='change_rsv_status'),
    url(r'^admin/t$', web_views.teacher_slot, name='slot'),
    url(r'^admin/d$', web_views.detail_slot, name='detail_slot'),

    url(r'^newrsv$', web_views.new_reservation, name='new_reservation'),
    url(r'^scode$', web_views.send_code, name='send_code'),

    # mobile pages
    url(r'^m/detail$', web_views.m_detail, name='m_detail'),
    url(r'^m/activity$', web_views.m_activity, name='m_activity'),
    url(r'^m/about$', web_views.m_about, name='m_about'),
    url(r'^m/teachers$', web_views.m_teachers, name='m_teachers'),
    url(r'^m/$', web_views.m_index, name='m_index'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
