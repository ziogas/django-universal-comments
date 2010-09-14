from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import gettext as _

class Comment(models.Model):
    
    STATUS_CHOICES = (
        (-1, _('Discarded')),
        (0, _('Waiting')),
        (1, _('Approved')),
    )
    
    name = models.CharField(max_length = 100, verbose_name = _('Name'))
    email = models.EmailField(verbose_name = _('Email address'))
    url = models.URLField(verbose_name = _('URL'), blank=True)
    comment = models.TextField(verbose_name = _('Comment'))
    ip = models.IPAddressField(verbose_name = _('IP'))
    created = models.DateTimeField(db_index=True, verbose_name = _('Created'))
    status = models.SmallIntegerField(choices = STATUS_CHOICES, db_index=True, verbose_name = _('Status'))
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.email)
    
    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
