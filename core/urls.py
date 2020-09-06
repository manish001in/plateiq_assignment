from django.conf.urls import url, include

from core import views

app_name = 'core'

urlpatterns = [
    url(r'^mark_status/$', views.mark_status, name='mark_status'),
    url(r'^update_invoice/', views.update_invoice_data, name='mark_status'),
]
