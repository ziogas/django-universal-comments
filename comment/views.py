from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from comment.models import Comment
from django.db import settings, models
from django import forms
from comment.form import CommentForm
from datetime import datetime

def save_comment(request):
    
    err = True

    try:
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.ip = request.META.get('REMOTE_ADDR', '')
        comment.created = datetime.today()
        comment.status = 0
        comment.save()

        err = False
        
    finally:
    
        if request.POST.get('ret'):
            ret = request.POST.get('ret')
        elif request.META.get('HTTP_REFERER'):
            ret = request.META.get('HTTP_REFERER')
        else:
            ret = '/'
       
        if err:
            ret += '?err=1'
            
        return HttpResponseRedirect(ret)
