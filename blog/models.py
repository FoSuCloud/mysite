from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField   #引入富文本编辑器
from read_statistics.models import ReadNumExpandMethod,ReadDetail  #导入阅读量
from django.urls import reverse

#博文分类的类
class BlogType(models.Model):
    type_name=models.CharField(max_length=15)
    # 在页面的显示名字
    def __str__(self):
        return self.type_name

#博文类
class Blog(models.Model,ReadNumExpandMethod):  #向模型引入阅读量,Blog类还继承了ReadNumExpandMethod类
    #get_read_num是ReadNumExpandMethod类的函数，但是在模型中引用了，所以也是个字段名
    title=models.CharField(max_length=50)
    blog_type=models.ForeignKey(BlogType,on_delete=models.CASCADE)
    content=RichTextUploadingField ()  #富文本
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    read_details=GenericRelation(ReadDetail)
    created_time=models.DateTimeField(auto_now_add=True)
    last_updated_time=models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('blog_detail',kwargs={'blog_pk':self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog: %s>" % self.title


    class Meta:
        ordering=['-created_time']  #-created_time符号表示倒序

