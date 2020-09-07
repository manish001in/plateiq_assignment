import json

from core.models import Invoice
from plateiq.common_utility import custom_serializer_object

mock_data = {
    'customer': 'XY Corporation', 'due_date': '2020-09-24', 'billing_address': 'XYZ Street, Q, Pincode:1234', 'tax_amount': '10.2', 
    'purchase_order_number': '1111', 'file_location': '/home/downloads/1/20200913_invoice.pdf', 'is_paid': False, 'created_date': '2020-09-13 11:49:12+00:00', 
    'invoice_date': '2020-09-11', 'vendor': 'ABC Inc', 'currency': 'US Dollars', 'is_digitized': True, 'due_amount': '150.20', 'notes': '', 'client_id': '103',
    'shipping_address': 'XYZ Street, Q, Pincode:1234', 'invoice_number': '123', 'modified_date': '2020-09-13 11:49:12+00:00', u'id': '1', 
    'discount_amount': '35.6', 'invoice_data': {
        '1': {'description':'Milk', 'quantity':10 ,'unit_price':4, 'amount':40, 'type':'Grocery', 'tax': None},
        '2': {'description':'Eggs', 'quantity':500 ,'unit_price':0.2, 'amount':100, 'type':'Grocery', 'tax': None}
    }
}

class InvoiceClass(object):
    '''
      Invoice class to interact with the invoice data, create various functions necessary to add/update/delete data and manipulate the invoice, digitize it etc.

    '''

    def __init__(self, pk=None):
        self.invoice = None
        if pk:
            if Invoice.objects.filter(pk=pk).exists():
                self.invoice = Invoice.objects.get(pk=pk)
        else:
            self.invoice = None

    def get_by_invoice_no(self, invoice_no):
        if Invoice.objects.filter(invoice_number=invoice_no).exists():
            self.invoice = Invoice.objects.get(invoice_number=invoice_no)

    def get_digitization_status(self):
        # the first variable returned represents if an invoice even exists
        if self.invoice is not None:
            return True, self.invoice.is_digitized
        else:
            return False, False

    def update_digitization_status(self, status_to_mark):
        
        if self.invoice is not None:
            self.invoice.is_digitized = status_to_mark
            self.invoice.save()
            return True
        else:
            return False

    def get_invoice_data(self):
        invoice_dict = {}
        if self.invoice is not None:
            invoice_dict = custom_serializer_object(self.invoice)
            invoice_dict['invoice_data'] = json.loads(invoice_dict['invoice_data'])

            invoice_dict = mock_data
            return True, invoice_dict
        else:
            return False, invoice_dict

    def update_invoice_data(self, update_dictionary):
        # returns True/False and error(if any)
        # the function updates invoice data, the dictionary can have any number of variables and whatever variable is present in it will get updated
        global mock_data

        invoice_obj = self.invoice
        fields = Invoice._meta.fields
        for field in fields:
            if field.name not in ['created_date', 'modified_date'] and field.name in update_dictionary:
                if isinstance(field, models.ForeignKey):
                    new_val = update_dictionary[field.name]
                    setattr(invoice_obj, field.name+'_id', new_val)

                elif field.name=='invoice_data':
                    new_invoice_data = update_dictionary['invoice_data']
                    old_invoice_data = json.loads(invoice_obj.invoice_data)

                    for i in new_invoice_data:
                        if i in old_invoice_data:
                            old_invoice_item = old_invoice_data[i]

                            for val in new_invoice_data[i]:
                                old_invoice_item[val] = new_invoice_data[i][val]
                            old_invoice_data[i] = old_invoice_item
                        else:
                            old_invoice_data[i] = new_invoice_data[i]
                    setattr(invoice_obj, field.name, json.dumps(old_invoice_data))
                else:
                    new_val = update_dictionary[field.name]
                    setattr(invoice_obj, field.name, new_val)
            invoice_obj.save()

    def initiate_automated_digitization(self):
        pass
        # if self.invoice is not None:
            # intitiate_digitization()
        #     return True/False
        # else:
        #     return False
        
    