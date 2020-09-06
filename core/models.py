# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
import datetime


# users of the system, inclduing clients and internal members
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_internal = models.BooleanField(default=False)
    company = models.ForeignKey(Customer, default=None, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.user.username

# possible currencies in the entire system
class Currency(models.Model):

    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

# Customer information, including subscription etc
class Customer(models.Model):
    pricing_plans = (
        ('Free', '0'),
        ('Basic', '10'),
        ('Premium', '30'),
        ('Custom', 'X')
    )

    name = models.CharField(max_length=1000)
    address = models.TextField()
    subscription_plan = models.CharField(choices=pricing_plans, default=pricing_plans[0][0], max_length=20)
    subscription_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, default='Miscellaneous')
    contact = models.CharField(max_length=15)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'address'))


# List of vendors information, for future analytics etc.
class Vendor(models.Model):

    name = models.CharField(max_length=1000)
    address = models.TextField()
    comment = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, default='Miscellaneous')
    contact = models.CharField(max_length=15)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'address'))

# The invoice and invoice data received from the customers
class Invoice(models.Model):

    invoice_number = models.CharField(max_length=100, null=True, default=None)
    purchase_order_number = models.CharField(max_length=100, null=True, blank=True, default=None)
    invoice_date = models.DateField(null=True, default=None)
    due_date = models.DateField(null=True, default=None)

    due_amount = models.DecimalField(max_digits=20, decimal_places=3, null=True, default=None)
    tax_amount = models.DecimalField(max_digits=20, decimal_places=3, null=True, default=None)
    discount_amount = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True, default=None)
    currency = models.ForeignKey(Currency, null=True, default=None)
    invoice_data = models.TextField(null=True, default=None)  # json value for the different services/products rendered
    is_paid = models.BooleanField(default=False)

    is_digitized = models.BooleanField(default=False)
    file_location = models.CharField(max_length=1500)  # could be a text field as well, specific to system

    customer = models.ForeignKey(Customer)
    vendor = models.ForeignKey(Vendor, null=True, default=None)
    customer_id = models.CharField(max_length=100, blank=True, null=True, default=None)
    
    billing_address = models.TextField(null=True, default=None)
    shipping_address = models.TextField(null=True, default=None)

    notes = models.TextField(blank=True, null=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.invoice_number

