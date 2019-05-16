import datetime
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Sum
from read_statistics.utils import get_seven_days_read_date,get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog

def get_seven_days_hot_blogs():
    today = timezone.now().date()  # 负号代表倒序
    date = today - datetime.timedelta(days=7)
    blogs=Blog.objects\
        .filter(read_details__date__lt=today,read_details__date__gte=date)\
        .values('id','title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type=ContentType.objects.get_for_model(Blog)
    dates,read_nums=get_seven_days_read_date(blog_content_type)

    #获取七天热门博客的缓存数据
    hot_data_for_seven_days=cache.get('hot_data_for_seven_days')
    if hot_data_for_seven_days is None:
        hot_data_for_seven_days=get_seven_days_hot_blogs()
        cache.set('get_seven_days_hot_blogs',hot_data_for_seven_days,36)  #记录3600秒的缓存数据

    context={}
    context['dates']=dates
    context['read_nums']=read_nums
    context['today_hot_data']=get_today_hot_data(blog_content_type)
    context['get_yesterday_hot_data']=get_yesterday_hot_data(blog_content_type)
    context['get_seven_days_hot_data']=hot_data_for_seven_days
    return render(request,'home.html',context)

