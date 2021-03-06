# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.test import TestCase
from core.utility import *
from core.models import *


class CoreFunctions(TestCase):
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

    def tests_a_invoice_status(self):

        with self.assertRaises(TypeError):
            invoice_status()

        self.assertEqual(invoice_status(self.invoice.id), False)
        self.assertEqual(invoice_status(self.invoice.id, True), True)
        self.assertEqual(invoice_status(self.invoice.id), True)

    def tests_b_invoice_data(self):

        with self.assertRaises(TypeError):
            invoice_data()
       
        self.mock_data = invoice_data(self.invoice.id)[1]
        self.assertEqual(invoice_data(self.invoice.id), (True, self.mock_data))

        update_dict = {'discount_amount': 40.600, 'invoice_data': {
                '1': {u'description': u'Juice', u'tax': None, u'unit_price': 4, u'amount': 40, u'type': u'Grocery', u'quantity': 10},
                '3': {u'description': u'Cheese', u'tax': None, u'unit_price': 2, u'amount': 2, u'type': u'Grocery', u'quantity': 1}
            }
        }

        self.assertEqual(invoice_data(self.invoice.id, update_dict), (True, ''))
        self.assertNotEqual(invoice_data(self.invoice.id), (True, self.mock_data))

        self.mock_data['discount_amount'] = "{:.3f}".format(40.6)
        self.mock_data['invoice_data']['1'] = update_dict['invoice_data']['1']
        self.mock_data['invoice_data']['3'] = update_dict['invoice_data']['3']

        self.mock_data.pop('modified_date')
        res, data = invoice_data(self.invoice.id)
        data.pop('modified_date')
        self.assertEqual((res, data), (True, self.mock_data))


class CoreFunctionsWeb(TestCase):
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

    def tests_a_mark_status(self):
        # testing getting the status
        response = self.client.get('/internal/mark_status?invoice_id='+str(self.invoice.id))
        self.assertEqual(response.status_code, 200)
        expected_data = {'result':True, 'invoice_id':self.invoice.id, 'invoice_no':'123', 'status':False}
        self.assertEqual(response.json(), expected_data)

        response = self.client.get('/internal/mark_status')
        self.assertEqual(response.status_code, 400)
        expected_data = {'result':False, 'error':"No invoice id sent."}
        self.assertEqual(response.json(), expected_data)

        # testing marking the status
        response = self.client.post('/internal/mark_status', {'invoice_id':str(self.invoice.id), 'status': True})
        self.assertEqual(response.status_code, 200)
        expected_data = {'result':True}
        self.assertEqual(response.json(), expected_data)

        response = self.client.post('/internal/mark_status', {'invoice_id':str(self.invoice.id)})
        self.assertEqual(response.status_code, 400)
        expected_data = {'result':False, 'error':"Empty status to mark"}
        self.assertEqual(response.json(), expected_data)

        response = self.client.post('/internal/mark_status', {})
        self.assertEqual(response.status_code, 400)
        expected_data = {'result':False, 'error':"No invoice id sent."}
        self.assertEqual(response.json(), expected_data)

    def tests_b_handle_invoice_data(self):
        
        # test which returns invoice_data
        response = self.client.get('/internal/handle_invoice?invoice_id='+str(self.invoice.id))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['result'], True)
        print "From tests_b_handle_invoice_data, getting all invoice data for id"
        print response.json()['data']

        # invalid id will raise error 500
        response = self.client.get('/internal/handle_invoice?invoice_id=7')
        self.assertEqual(response.status_code, 500)

        self.assertEqual(response.json()['result'], False)

        # testing post request to handle invoice to update/add one/more values
        response = self.client.post('/internal/handle_invoice', {'invoice_id':str(self.invoice.id)})
        self.assertEqual(response.status_code, 400)
        expected_data = {'result':False, 'error':"No invoice id/invoice data sent."}
        self.assertEqual(response.json(), expected_data)

        response = self.client.post('/internal/handle_invoice', {})
        self.assertEqual(response.status_code, 400)
        expected_data = {'result':False, 'error':"No invoice id/invoice data sent."}
        self.assertEqual(response.json(), expected_data)

        update_dict = {'discount_amount': 40.600, 'invoice_data': {
                '1': {u'description': u'Juice', u'tax': None, u'unit_price': 4, u'amount': 40, u'type': u'Grocery', u'quantity': 10},
                '3': {u'description': u'Cheese', u'tax': None, u'unit_price': 2, u'amount': 2, u'type': u'Grocery', u'quantity': 1}
            }
        }

        response = self.client.post('/internal/handle_invoice', {'invoice_id':str(self.invoice.id), 'invoice_data': str(update_dict)})
        self.assertEqual(response.status_code, 400)
        # fails because update_dictionary is not provided as a proper json string.
        self.assertEqual(response.json()['result'], False)


        response = self.client.post('/internal/handle_invoice', {'invoice_id':str(self.invoice.id), 'invoice_data': json.dumps(update_dict)})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['result'], True)

        # using this we will compare if our values were updated
        response = self.client.get('/internal/handle_invoice?invoice_id='+str(self.invoice.id))
        invoice_data = response.json()['data']

        self.assertEqual(invoice_data['discount_amount'], "{:.3f}".format(update_dict['discount_amount']))
        self.assertEqual(invoice_data['invoice_data']['1'], update_dict['invoice_data']['1'])
        self.assertEqual(invoice_data['invoice_data']['3'], update_dict['invoice_data']['3'])
