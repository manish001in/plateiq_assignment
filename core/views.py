# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

import logging, datetime, os, re, json

# from config import SELFLOCATION, STATIC_FILES_DIR, LOGSLOCATION
from core.models import *


