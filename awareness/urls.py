from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^awareness/vulnerability/add/$', views.addVuln),
    url(r'^awareness/vulnerability/delete/$', views.dropVuln),
    url(r'^awareness/vulnerability/update/$', views.updateVuln),
    url(r'^awareness/vulnerability/pie/get/$', views.getVuln_pie),
    url(r'^awareness/vulnerability/line/get/$', views.getVuln_line),

]