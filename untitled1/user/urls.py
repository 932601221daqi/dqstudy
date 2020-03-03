from django.conf.urls import url
from user import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
        url(r'^register$', views.RegisterView.as_view(), name='register'), #注册
        url(r'^login$', views.LoginView.as_view(), name='login'),  # 登陆
        url(r'^logout$', login_required(views.LogoutView.as_view()), name='logout'),  # 推出
        url(r'^center$', login_required(views.UserCenter.as_view()), name='center'),  # 中心

]
