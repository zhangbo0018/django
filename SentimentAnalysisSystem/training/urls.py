"""
URL configuration for detection.

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
from training import views

app_name = 'training'
urlpatterns = [
    # 上传测试集
    re_path(r'^upload/$', views.Upload.as_view(), name='upload'),
    # 情感分析
    re_path(r'^sentiment_analysis/$', views.SentimentAnalysis.as_view(), name='sentiment_analysis'),
    # # 下载预测结果
    # re_path(r'^download/$', views.download, name='download'),
    # 展示数据集
    re_path(r'^display_dataset/$', views.display_dataset, name='display_dataset'),
]
