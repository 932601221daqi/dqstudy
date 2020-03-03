from django.shortcuts import render, HttpResponse
from django.views import View
from text.models import TextType, TextContext
from django.core.paginator import Paginator
from django_redis import get_redis_connection


# Create your views here.
# /index
class IndexView(View):
    def get(self, request, *args, **kwargs):
        '''显示首页'''

        # 查询课程分类
        types = TextType.objects.all()

        # 组织上下文
        context = {
            'types': types
        }

        # 组织模板
        return render(request, 'index.html', context)


# /text/course
class CourseView(View):
    def get(self, request, *args, **kwargs):
        # 获取课程类型id和页码
        course_id = kwargs.get('course_id')
        course_page = kwargs.get('course_page')

        # 进行数据查找
        contexts = TextContext.objects.filter(type=course_id)

        # 进行分页的处理
        paginator = Paginator(contexts, 30)

        # 获取第page页的内容
        try:
            page = int(course_page)
        except Exception as e:
            page = 1
        # 如果页码大于总页数
        if page > paginator.num_pages:
            page = 1
        # 获取第course_page页的page对象
        course_page = paginator.page(page)

        # 1.总页数小于五页，显示所有页码
        # 2.当前页是前三页,显示1-5
        # 3.当前页是后三页，显示后五页
        # 4.其他情况，显示当前页前俩后俩
        number_pages = paginator.num_pages

        # 组织上下文
        context = {
            'course_id': course_id,
            'course_page': course_page,
            'page': page,
            'number_pages': number_pages,

        }

        return render(request, 'course.html', context)


class ContentView(View):
    def get(self, request, *args, **kwargs):
        # 获取内容id
        content_id = kwargs.get('content_id')
        # 获取数据
        page_context = TextContext.objects.get(id=int(content_id))

        # 添加历史浏览
        # 获取用户名
        user = request.user
        # 获取redis链接
        conn = get_redis_connection('default')
        history_key = 'history_%d' % user.id
        # 查看历史中有无此项,有的话删除
        conn.lrem(history_key, 0, content_id)
        # 将历史记录从左侧插入
        conn.lpush(history_key, content_id)
        # 进行数据修剪华南，保留最新的10个
        conn.ltrim(history_key, 0, 9)

        return render(request, 'course_content.html', {'page_context': page_context})
