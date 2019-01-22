from django.conf.urls import url
from . import views

urlpatterns = [
    # 设备管理部分
    url(r'^local/device/add/$', views.addDevice),
    url(r'^local/device/connection/add/$', views.addConnection),
    url(r'^local/device/delete/$', views.dropDevice),
    url(r'^local/device/all/delete/$', views.dropAllDevice),
    url(r'^local/device/connections/delete/$', views.dropConnection),
    url(r'^local/device/update/$', views.updateDevice),
    url(r'^local/device/connections/update/$', views.updateConnection),
    url(r'^local/device/list/get/$', views.getDeviceList),
    url(r'^local/device/detail/get/$', views.getDeviceDesc),
    url(r'^local/device/connections/get/$', views.getDeviceConnection),
    # 攻击工具部分
    url(r'^local/attack/demonstrate/$', views.attackDemo),
    url(r'^local/attack/tools/args/get/$', views.getAttackArg),
    url(r'^local/attack/history/get/$', views.getHistories),
    url(r'^local/attack/history/delete/$', views.deleteHistory),
    url(r'^local/attack/history/empty/$', views.emptyHistory),
    url(r'^local/attack/demo/initialize/$', views.demoInit),
    url(r'^local/attack/tools/initialize/$', views.toolsInit),
    # 攻击脚本部分
    url(r'^local/attack/scripts/initialize/$', views.scriptsInit),
    url(r'^local/attack/script/add/$', views.addScript),
    url(r'^local/attack/script/delete/$', views.deleteScript),
    url(r'^local/attack/script/get/$', views.getScripts),

]