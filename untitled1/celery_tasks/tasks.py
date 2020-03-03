# 使用celery
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, RequestContext
from django.shortcuts import render

# 在任务处理者一端加，环境初始化
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled1.settings")
django.setup()  # 以上四句如果celery在别的机器上在那个机器上加

# 创建一个celery的实例对象
app = Celery('celery_tasks.tasks', broker='redis://192.168.70.128:6379/6')


# 定义发生邮件函数
@app.task
def send_email(to_email, username):
    # 组织邮件信息
    subject = '来自dq_study'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s,欢迎您成为dq_study的用户！</h1>' % username
    send_mail(subject, message, sender, receiver, html_message=html_message)
