from django.conf.urls import url
from text import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^index$', login_required(views.IndexView.as_view()), name='index'),  # 显示首页
    url(r'^course/(?P<course_id>\d+)/(?P<course_page>\d+)$', login_required(views.CourseView.as_view()), name='course'),
    url(r'^content/(?P<content_id>\d+)$', login_required(views.ContentView.as_view()), name='content')
]
