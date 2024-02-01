from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path
from django.views.static import serve
from django.conf.urls import handler500

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


    path('admin/', admin.site.urls),
    path('',include('todo_app.urls')),
    
    
    
]

handler404='todo_app.views.handling_404'
handler500 = 'todo_app.views.custom_500'

