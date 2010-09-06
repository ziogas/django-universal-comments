from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('comment.views',
    url(r'^save$', 'save_comment', name='comment-save'),
)