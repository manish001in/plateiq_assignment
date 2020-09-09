# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging, datetime, os, re, json

from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

# from config import SELFLOCATION, STATIC_FILES_DIR, LOGSLOCATION
from core.models import *
from utility import upload_file
from customer.invoice import InvoiceClass

@require_http_methods(['GET'])
def invoice_status(request, invoice_id):

    invoice_obj = InvoiceClass(invoice_id)
    return JsonResponse({'result':True, 'invoice_id':invoice_obj.invoice.id, 'invoice_no':invoice_obj.invoice.invoice_number, 'status':invoice_obj.invoice.is_digitized})
       

@require_http_methods(['GET'])
def invoice_data(request, invoice_id):
    # returns a json form of invoice data, the keys can be used to send back data to update
    invoice_obj = InvoiceClass(invoice_id)

    if invoice_obj.invoice.is_digitized:
        result, invoice_data = invoice_obj.get_invoice_data()
        return JsonResponse({'result':result, 'invoice_id':invoice_obj.invoice.id, 'invoice_no':invoice_obj.invoice.invoice_number, 'data': invoice_data})

    else:
        return JsonResponse({'result':False, 'invoice_id':invoice_obj.invoice.id, 'invoice_no':invoice_obj.invoice.invoice_number, 'error': "The document has not been digitized yet."})


@require_http_methods(['POST'])
def upload_invoice(request):
    if request.FILES:
        doc = request.FILES['file']
        if "pdf" not in doc.content_type:
            return JsonResponse({'result': False, 'error': "The document is not a pdf file. Please upload a pdf file"}, status=400)
        else:
            customer_id = request.POST.get('customer', '')

            if customer_id!='' and Customer.objects.filter(id=customer_id).exists():
                customer = Customer.objects.get(id=customer_id)
                result, file_path = upload_file(request.FILES['file'].name, customer.name, customer_id, request.FILES['file'])

                if result:
                    invoice_obj = Invoice.objects.create(file_location=file_path, customer=customer)
                    return JsonResponse({'result':True, 'invoice_id':invoice_obj.id})
                else:
                    return JsonResponse({'result':False, 'error':"Some error occured in uploading, please try again"}, status=500)
            else:
                return JsonResponse({'result':False, 'error':"Customer does not exist."}, status=404)

    else:
        return JsonResponse({'result': False, 'error': "No file uploaded."}, status=400)