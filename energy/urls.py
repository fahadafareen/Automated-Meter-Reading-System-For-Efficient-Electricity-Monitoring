"""energy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.first,name='first'),
    path('dash/', views.dash, name='dash'),
    path('billss/',views.billss,name='billss'),
    path('viewcon/',views.viewcons,name='viewcon'),
    path('conss/',views.conss,name='conss'),
    path('logout/',views.logout,name='logout'),
    path('viewbill/',views.viewbill,name='viewbill'),
    path('addreg/', views.addreg, name='addreg'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logint/',views.logint,name='logint'),
    path('index/',views.dash,name='index'),
    path('addelect/',views.addelect,name='addelect'),
    path('addcon/',views.addcon,name='addcon'),
    path('addanal/',views.addanal,name='addanal'),
    path('addbill/',views.addbill,name='addbill'),
    path('addnews/',views.addnews,name='addnews'),
    path('newss/',views.newss,name='newss'),
    path('analyze/',views.analyze,name='analyze'),
    path('mtr/',views.mtr,name='mtr'),
    path('com/',views.com,name='com'),
    path('comp/',views.comp,name='comp'),
    path('cusview/',views.cusview,name='cusview'),
    path('curnew/',views.curnew,name='curnew'),
    path('curprof/',views.curprof,name='curprof'),
    path('vbill/',views.vbill,name='vbill'),
    path('pay/',views.pay,name='pay'),
    path('paybill/<int:id>/',views.paybill,name='paybill'),
    path('paybill/pay/',views.pay,name='pay'),
    path('viewel/',views.viewel,name='viewel'),
    path('viewconsumerpayment/',views.viewconsumerpayment,name='viewconsumerpayment'),
    path('accept_bill/<int:id>/', views.accept_bill, name='accept_bill'),
    path('reject_bill/<int:id>/', views.reject_bill, name='reject_bill'),
    path('user_chat/', views.user_chat, name='user_chat'),
    path('admin_chat/', views.admin_chat, name='admin_chat'),
    path('analysis_graph/', views.analysis_graph, name='analysis_graph'),
    path('zone_status/', views.zone_status, name='zone_status'),
    path('add_zone/', views.add_zone, name='add_zone'),
    path('dispatch_worker/', views.dispatch_worker, name='dispatch_worker'),
    path('view_dispatch/', views.view_dispatch, name='view_dispatch'),
    path('admin_view_complaints/', views.admin_view_complaints, name='admin_view_complaints'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),
    path('delete_news/<int:id>/', views.delete_news, name='delete_news'),
    path('accept_request/<str:rtype>/<int:id>/', views.accept_request, name='accept_request'),
    path('reject_request/<str:rtype>/<int:id>/', views.reject_request, name='reject_request'),
    path('simulate_monitoring/', views.admin_simulate_monitoring, name='admin_simulate_monitoring'),

    path('worker_dash/', views.worker_dash, name='worker_dash'),
    path('worker_tasks/', views.worker_tasks, name='worker_tasks'),
    path('update_dispatch_status/', views.update_dispatch_status, name='update_dispatch_status'),
    path('submit_report/', views.submit_report, name='submit_report'),

    path('consumer_dash/', views.consumer_dash, name='consumer_dash'),
    path('new_connection/', views.new_connection, name='new_connection'),
    path('solar_connection/', views.solar_connection, name='solar_connection'),
    path('name_change/', views.name_change, name='name_change'),
    path('tariff_change/', views.tariff_change, name='tariff_change'),
    path('track_requests/', views.track_requests, name='track_requests'),
    path('download_receipt/<int:id>/', views.download_receipt, name='download_receipt'),
    path('payment_history/', views.payment_history, name='payment_history'),
    path('energy_monitoring/', views.energy_monitoring, name='energy_monitoring'),
    path('get_energy_data/', views.get_energy_data, name='get_energy_data'),
    path('get_admin_monitoring_data/', views.get_admin_monitoring_data, name='get_admin_monitoring_data'),
    path('get_meter_usage/', views.get_meter_usage, name='get_meter_usage'),

    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
