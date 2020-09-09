# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging, datetime, os, re, json

from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

from core.models import *
from customer.invoice import InvoiceClass

@require_http_methods(['GET', 'POST'])
def mark_status(request):
    # used to get and update digitization status
    if request.method == "GET":
        invoice_id = request.GET['invoice_id'] if 'invoice_id' in request.GET else ''
        if invoice_id!='':
            invoice_obj = InvoiceClass(invoice_id)
            return JsonResponse({'result':True, 'invoice_id':invoice_obj.invoice.id, 'invoice_no':invoice_obj.invoice.invoice_number, 'status':invoice_obj.invoice.is_digitized})
        else:
            return JsonResponse({'result':False, 'error': "No invoice id sent."}, status=400)
    
    else:
        invoice_id = request.POST.get('invoice_id', '')
        status = request.POST.get('status', '')

        if invoice_id!='':
            invoice_obj = InvoiceClass(invoice_id)
            response = False
            if status!='':
                response = invoice_obj.update_digitization_status(status)
                return JsonResponse({'result':response})
            else:
                return JsonResponse({'result':response, 'error': "Empty status to mark"}, status=400)
        else:
            return JsonResponse({'result':False, 'error': "No invoice id sent."}, status=400)

# function for getting/updating invoice data
@require_http_methods(['GET', 'POST'])
def handle_invoice_data(request):

    if request.method == "GET":
        invoice_id = request.GET['invoice_id'] if 'invoice_id' in request.GET else ''
        if invoice_id!='':
            invoice_obj = InvoiceClass(invoice_id)
            result, invoice_data = invoice_obj.get_invoice_data()

            if result:
                return JsonResponse({'result':result, 'invoice_id':invoice_obj.invoice.id, 'invoice_no':invoice_obj.invoice.invoice_number, 'data': invoice_data})
            else:
                return JsonResponse({'result':result, 'invoice_id':invoice_obj.invoice.id, 'invoice_no':invoice_obj.invoice.invoice_number, 'error': "Invoice data fetch error"})

        else:
            return JsonResponse({'result':False, 'error': "No invoice id sent."}, status=400)
    
    else:
        invoice_id = request.POST.get('invoice_id', '')
        updated_invoice_dict = request.POST.get('invoice_data', '')

        if invoice_id!='' and updated_invoice_dict!='':
            invoice_obj = InvoiceClass(invoice_id)
            # to handle data coming from the frontend
            try:
                if type(updated_invoice_dict)!=type(dict):
                    updated_invoice_dict = json.loads(updated_invoice_dict)
            except Exception as e:
                return JsonResponse({'result':False, 'error': "Invalid data. "+str(e)}, status=400)

            response, error = invoice_obj.update_invoice_data(updated_invoice_dict)
            if response:
                return JsonResponse({'result':response})
            else:
                return JsonResponse({'result':response, 'error': "Error in updating invoice data, {}".format(error)})

        else:
            return JsonResponse({'result':False, 'error': "No invoice id/invoice data sent."}, status=400)