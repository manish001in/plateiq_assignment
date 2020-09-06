from django.conf.urls import url, include

from customer import views

app_name = 'customer'

urlpatterns = [
    url(r'^upload_invoice/$', views.upload_invoice, name='upload_invoice'),
    url(r'^invoice_status/^(?P<invoice_id>\w+)/', views.invoice_status, name='invoice_status'),
    url(r'^invoice_data/^(?P<invoice_id>\w+)/', views.invoice_data, name='invoice_data')
]
