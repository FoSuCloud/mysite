from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

#路由设置
urlpatterns = [
    #首页此时显示第一篇文章内容
    path('',views.home,name='home'),  #设置别名home
    path('admin/', admin.site.urls),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('blog/',include('blog.urls')), #引用blog页面的urls
    path('comment/',include('comment.urls')),
    path('likes/', include('likes.urls')),
    path('user/',include('user.urls')),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
