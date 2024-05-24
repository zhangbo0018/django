"""
URL configuration for user.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path, path
from user import views

app_name = 'user'
urlpatterns = [
    # 展示用户列表
    re_path(r'^display_user/$', views.display_user, name='display_user'),
    # 上传测试集进行用户画像
    re_path(r'^user_portrait/$', views.UserPortrait.as_view(), name='user_portrait'),
    # 注册用户
    re_path(r'^register/$', views.UserRegister.as_view(), name='register'),
    # 执行个性化推荐
    re_path(r'^recommend/$', views.PersonalizedRecommendation.as_view(), name='recommend'),
    # 展示个性化推荐结果
    re_path(r'^display_recommend/$', views.display_recommend, name='display_recommend'),
    # 个性化推荐反馈
    re_path(r'^display_feedback/$', views.RecommendationFeedback.as_view(), name='display_feedback'),
    # 用户画像可视化
    re_path(r'^visualization/$', views.visualization, name='visualization'),
]
