# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.test import TestCase
from plateiq.settings import BASE_DIR
from core.models import *

class CustomerFunctionsWeb(TestCase):
    def setUp(self):
        user = User.objects.create_user('test_user', 'test@123.com', 'test123')
        curr = Currency.objects.create(name='US Dollars', symbol='USD')
        cust = Customer.objects.create(name='Test Customer', address='Test St, City X, Pincode-1234', contact='9999999999')
        UserProfile.objects.create(user=user, is_internal=True, company=cust)
        vendor = Vendor.objects.create(name='Test Vendor', address='Vendor Lane, City Y, Pincode-6666', contact='6666666666')

        data = {
            '1': {'description':'Milk', 'quantity':10 ,'unit_price':4, 'amount':40, 'type':'Grocery', 'tax': None},
            '2': {'description':'Eggs', 'quantity':500 ,'unit_price':0.2, 'amount':100, 'type':'Grocery', 'tax': None}
        }

        self.mock_data = {'customer': 'Test Customer', 'due_date': '2020-09-24', 'billing_address': 'XYZ Street, Q, Pincode:1234', 
        'tax_amount': '10.200', 'purchase_order_number': '1111', 'file_location': '/home/downloads/1/20200913_invoice.pdf', 'is_paid': 'False', 
        'created_date': '2020-09-08 22:44:44.922061+00:00', 'invoice_date': '2020-09-11', 'vendor': 'Test Vendor', 'currency': 'US Dollars', 
        'is_digitized': 'False', 'due_amount': '150.200', 'notes': 'Test invoice data', 'client_id': 'None', 'shipping_address': 'XYZ Street, Q, Pincode:1234', 
        'invoice_number': '123', 'modified_date': '2020-09-08 22:44:44.922148+00:00', u'id': '7', 'discount_amount': '35.600', 
        'invoice_data': {u'1': {u'description': u'Milk', u'tax': None, u'unit_price': 4, u'amount': 40, u'type': u'Grocery', u'quantity': 10}, u'2': {u'description': u'Eggs', u'tax': None, u'unit_price': 0.2, u'amount': 100, u'type': u'Grocery', u'quantity': 500}}}

        self.maxDiff = None
        data_str = json.dumps(data)

        self.invoice = Invoice.objects.create(invoice_number='123', purchase_order_number='1111', invoice_date='2020-09-11', due_date='2020-09-24', 
        due_amount='150.20', tax_amount='10.2', discount_amount='35.6', currency=curr, file_location='/home/downloads/1/20200913_invoice.pdf', 
        customer=cust, vendor=vendor, billing_address='XYZ Street, Q, Pincode:1234', shipping_address='XYZ Street, Q, Pincode:1234', 
        notes='Test invoice data', invoice_data=data_str)

        self.invoice2 = Invoice.objects.create(invoice_number='456', purchase_order_number='1111', invoice_date='2020-09-11', due_date='2020-09-24', 
        due_amount='150.20', tax_amount='10.2', discount_amount='35.6', currency=curr, file_location='/home/downloads/1/20200913_invoice2.pdf', 
        customer=cust, vendor=vendor, billing_address='XYZ Street, Q, Pincode:1234', shipping_address='XYZ Street, Q, Pincode:1234', 
        notes='Test invoice data', invoice_data=data_str, is_digitized=True)


    def tests_a_invoice_status(self):
        # testing getting the status for the customer
        response = self.client.get('/customer/invoice_status/'+str(self.invoice.id)+'/')
        self.assertEqual(response.status_code, 200)
        expected_data = {'result':True, 'invoice_id':self.invoice.id, 'invoice_no':'123', 'status':False}
        self.assertEqual(response.json(), expected_data)

        response = self.client.get('/customer/invoice_status/111/')
        self.assertEqual(response.status_code, 500)
        
        self.assertEqual(response.json()['result'], False)


    def tests_b_getting_invoice_data(self):
        # testing getting invoice data if it is digitized

        response = self.client.get('/customer/invoice_data/'+str(self.invoice.id)+'/')
        self.assertEqual(response.status_code, 200)
        expected_data = {'result':False, 'invoice_id':self.invoice.id, 'invoice_no':'123', 'error': "The document has not been digitized yet."}
        self.assertEqual(response.json(), expected_data)

        response = self.client.get('/customer/invoice_data/'+str(self.invoice2.id)+'/')
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.json()['result'], True)
        self.assertEqual(response.json()['invoice_id'], self.invoice2.id)
        self.assertEqual(response.json()['invoice_no'], '456')

        print "Invoice data for customer test: tests_b_getting_invoice_data"
        print response.json()['data']

        response = self.client.get('/customer/invoice_data/111/')
        self.assertEqual(response.status_code, 500)
        
        self.assertEqual(response.json()['result'], False)        


    def tests_c_upload_document(self):
        # we will test things related to file uploading here.

        response = self.client.get('/customer/upload_invoice/')
        # 405 cos we have not allowed a get request to this method
        self.assertEqual(response.status_code, 405)
        
        response = self.client.post('/customer/upload_invoice/')
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(response.json()['result'], False)
        self.assertEqual(response.json()['error'], "No file uploaded.")

        # not a pdf file        
        with open(BASE_DIR+'/test1.xyz', 'rb+') as attch:
            response = self.client.post('/customer/upload_invoice/', {'file': attch})
            self.assertEqual(response.json()['result'], False)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()['error'], "The document is not a pdf file. Please upload a pdf file")


        with open(BASE_DIR+'/test.pdf', 'rb+') as attch:
            response = self.client.post('/customer/upload_invoice/', {'file': attch, 'customer': self.invoice.customer.id})
            self.assertEqual(response.status_code, 200)
            
            response = self.client.post('/customer/upload_invoice/', {'file': attch, 'customer': -23})
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()['error'], "Customer does not exist.")