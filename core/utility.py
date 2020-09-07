from customer.invoice import InvoiceClass

# the following function can be used by a microservice to update/get digitization status
def invoice_status(invoice_id, status=None):
    try:

        if status:
            invoice_obj = InvoiceClass(invoice_id)
            response = invoice_obj.update_digitization_status(status)
            return response
        else:
            invoice_obj = InvoiceClass(invoice_id)
            return invoice_obj.invoice.is_digitized

    except Exception as e:
        logger.error("Error raised in invoice_status "+str(e))
        return False

# the following function can be used by a microservice to update/get invoice data
def invoice_data(invoice_id, update_dictionary=None):
    try:

        if update_dictionary:
            invoice_obj = InvoiceClass(invoice_id)
            response, error = invoice_obj.update_invoice_data(update_dictionary)
            return response, error
        else:
            invoice_obj = InvoiceClass(invoice_id)            
            return True, invoice_obj.get_invoice_data()

    except Exception as e:
        logger.error("Error raised in invoice_data "+str(e))
        return False, "Error raised in invoice_data "+str(e)