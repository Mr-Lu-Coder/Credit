# coding:utf-8 #
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django import forms
from django.template import RequestContext
from grade import Course,NPU
# Create your views here.
import ConfigParser

import logging
logger = logging.getLogger('xzs')

def login(req):
    if req.method == 'POST':
        return render_to_response('index.html')
    else:
        return render_to_response('login.html',context_instance=RequestContext(req))

def index(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        npu = NPU(username, password)
        term_list = npu.getGrades(npu.getPage())
        sum,weight = npu.getCredit(term_list)
        creditProduct = 0
        error = ''
        if weight == 0:
            creditProduct = 0
        else:
            creditProduct = float('%.3f' %(sum/weight))
        if term_list == None or len(term_list) == 0:
            logger.info('login error in view')
            error = '请检查学号和密码是否有误'
        else:
            logger.info(username+'login success!')
            pass
        #print error,term_list
        return render_to_response('index.html', locals())
    else:
        return HttpResponseRedirect('login.html',context_instance=RequestContext(req))
# def debug(req):
#     if req.method == 'POST':
#         return render_to_response('index.html')
#     else:
#         return render_to_response('debug.html',context_instance=RequestContext(req))