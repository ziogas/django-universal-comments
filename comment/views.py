from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from comment.models import Comment
from django.db import settings, models
from django import forms
from comment.form import CommentForm
from datetime import datetime
from django.core.mail import send_mail
from django.utils.translation import gettext as _

def save_comment(request):
    
    err = True
    
    comment_status = 0
    
    try:
        if request.POST['private_comment']:
            comment_status = -2
    except:
        pass

    try:
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.ip = request.META.get('REMOTE_ADDR', '')
        comment.created = datetime.today()
        comment.status = comment_status
        comment.save()
        
        err = False
        
        if comment_status == -2 or settings.COMMENT_NOTIFICATION_EMAIL:
            send_mail( _('Comment')+': '+comment.name, comment.comment, comment.email, [settings.COMMENT_NOTIFICATION_EMAIL], fail_silently=True)
        
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
