import os
from django import template, forms
from django.template.defaultfilters import slugify
from comment.form import CommentForm
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.template import RequestContext

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
    
    return ret

@register.inclusion_tag('comment_list.html')
def comment_list(obj):
    object_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type__pk=object_type.id, object_id=obj.id, status__gt=-1)
    
    return {'comments': comments}