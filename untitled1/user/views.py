from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views import View
from user.models import User
from text.models import TextContext
from django_redis import get_redis_connection
import re
from celery_tasks.tasks import send_email


# Create your views here.
# /user/register
class RegisterView(View):
    '''显示注册界面'''

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 数据校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整！'})
        # 邮箱校验
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确！'})
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议！'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户不存在
            user = None
        if user:
            # 如果已存在 #如果已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在！'})
        # 业务处理：用户注测
        # 使用django内置的用户处理
        user = User.objects.create_user(username, email, password)
        user.is_active = 1
        user.save()

        # 使用celery发出发邮件任务
        send_email.delay(email, username)

        # 使用反向解析返回登陆界面
        return redirect(reverse('user:login'))


# user/login
class LoginView(View):
    '''显示'''

    def get(self, request, *args, **kwargs):
        '''显示登陆界面'''
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request, *args, **kwargs):
        '''进行登陆'''
        # 接受数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据填写不完整'})
        # 业务处理，登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户正确
            # 记录用户的登录状态
            login(request, user)
            response = redirect(reverse('text:index'))
            # 判断是否需要记住用户名
            remember = request.POST.get('remember')
            if remember == 'on':
                # 记住用户名
                response.set_cookie('username', username, max_age=14 * 7 * 3600)
            else:
                response.delete_cookie('username')

            # 返回response
            return response

        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


# user/logout
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        '''认证系统的退出'''
        # 清除用户的session信息
        logout(request)
        # 跳转到登陆页面
        return redirect(reverse('user:login'))


class UserCenter(View):
    '''用户中心页面'''

    def get(self, request, *args, **kwargs):
        # 获取用户信息
        user = request.user
        # 获取链接
        conn = get_redis_connection('default')
        # 获取key
        history_key = 'history_%d' % user.id
        # 查找浏览记录
        content_history = conn.lrange(history_key, 0, 9)

        #遍历获取文章信息,添加到列表中
        content_list = []
        for id in content_history:
            content = TextContext.objects.get(id=id)
            content_list.append(content)



        return render(request, 'center.html', {'content_list':content_list})