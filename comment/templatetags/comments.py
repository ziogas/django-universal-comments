import os
from django import template, forms
from django.template.defaultfilters import slugify
from comment.form import CommentForm
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.template import RequestContext
from django.db import settings

register = template.Library()

@register.inclusion_tag('comment_form.html', takes_context=True)
def comment_form(context, obj):
    object_type = ContentType.objects.get_for_model(obj)
    
    form = CommentForm()
    form.fields['content_type'].initial = object_type.id
    form.fields['object_id'].initial = obj.pk
    form.fields['content_type'].widget = forms.HiddenInput()
    form.fields['object_id'].widget = forms.HiddenInput()
    
    #TODO: normal validation
#    if context['request'] and context['request'].GET.get('err'):
#        ret = {'err': _('Some fields contain errors') ,'form': form}
#    else:
    ret = {'form': form}
    
    try:
        if settings.COMMENT_ALLOW_PRIVATE_COMMENTS:
            ret['private_comments'] = True
    except:
        pass
    
    return ret

@register.inclusion_tag('comment_list.html')
def comment_list(obj):
    
    try:
        if settings.COMMENT_SHOW_STATUS:
            status = int(settings.COMMENT_SHOW_STATUS)
    except:
        status = -1
        
    object_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type__pk=object_type.id, object_id=obj.id, status__gt=status)
    
    return {'comments': comments}