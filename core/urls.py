from django.conf.urls import url, include

from core import views

app_name = 'core'

urlpatterns = [
    url(r'^mark_status$', views.mark_status, name='mark_status'),
    url(r'^handle_invoice', views.handle_invoice_data, name='handle_invoice'),
]
