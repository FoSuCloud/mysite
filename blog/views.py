from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import Blog,BlogType
from read_statistics.utils import read_statistics_once_read

def get_blog_list_common_date(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)  # 默认打开第一页,获取页码参数
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 只显示当前范围五页
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages)+1))
    # 加上省略页码标识
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获取日期归档对应的博客数量
    blog_dates=Blog.objects.dates('created_time','month',order='DESC')
    blog_dates_dict={}
    for blog_date  in blog_dates:
        blog_count=Blog.objects.filter(created_time__year=blog_date.year,
                            created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date]=blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    # 获取博客分类的对应的博客数量
    context['blog_types'] =BlogType.objects.annotate(blog_count=Count('blog'))
    # DESC表示倒序,按月分类
    context['blog_dates'] = blog_dates_dict
    return context

#把数据库内容返回到模板html页面
def blog_list(request):
    blogs_all_list=Blog.objects.all()
    context=get_blog_list_common_date(request,blogs_all_list)
    #完整路径是mysite/templatetags/blog/blog_list.html
    return render(request,'blog/blog_list.html',context)

def blogs_with_type(request,blog_type_pk):
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_date(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request,'blog/blogs_with_type.html',context)

def blogs_with_date(request,year,month):
     #created_time__year这是两条横线，因为filter筛选器
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_date(request,blogs_all_list)
    context['blogs_with_date']='%s年%s月' %(year,month)
    return render(request,'blog/blogs_with_date.html', context)

#blog_pk关键词
def blog_detail(request,blog_pk):
    blog=get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key=read_statistics_once_read(request,blog)

    context={}
    context['previous_blog']=Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog']=Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog']=blog   #当前blog
    response=render(request,'blog/blog_detail.html',context)   #获得的响应
    #max_age=60表示60秒内有效
    response.set_cookie(read_cookie_key,'true')   #提醒浏览器保存相关信息,阅读cookie标记
    return response

