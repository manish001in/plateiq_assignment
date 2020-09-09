import os, json

from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'plateiq.settings'
application = get_wsgi_application()

from core.models import *

user = User.objects.create_user('test_user1', 'test@123.com', 'test123')
curr = Currency.objects.create(name='US Dollars', symbol='USD')
cust = Customer.objects.create(name='Test Customer', address='Test St, City X, Pincode-1234', contact='9999999999')
UserProfile.objects.create(user=user, is_internal=True, company=cust)
vendor = Vendor.objects.create(name='Test Vendor', address='Vendor Lane, City Y, Pincode-6666', contact='6666666666')

data = {
    '1': {'description':'Milk', 'quantity':10 ,'unit_price':4, 'amount':40, 'type':'Grocery', 'tax': None},
    '2': {'description':'Eggs', 'quantity':500 ,'unit_price':0.2, 'amount':100, 'type':'Grocery', 'tax': None}
}

data_str = json.dumps(data)

invoice = Invoice.objects.create(invoice_number='123', purchase_order_number='1111', invoice_date='2020-09-11', due_date='2020-09-24', 
due_amount='150.20', tax_amount='10.2', discount_amount='35.6', currency=curr, file_location='/home/downloads/1/20200913_invoice.pdf', 
customer=cust, vendor=vendor, billing_address='XYZ Street, Q, Pincode:1234', shipping_address='XYZ Street, Q, Pincode:1234', 
notes='Test invoice data', invoice_data=data_str)