import os

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
import pandas as pd
import jieba
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
# Create your views here.


# 上传数据集
class Upload(View):
    """上传测试集"""

    def get(self, request):
        if os.listdir(settings.MEDIA_ROOT):
            # 检测之前情况上一次检测的残留图片
            for f in os.listdir(settings.MEDIA_ROOT):
                file_p = os.path.join(settings.MEDIA_ROOT, f)
                try:
                    if os.path.isfile(file_p):
                        os.remove(file_p)
                except:
                    pass
        return render(request, 'training/training-upload.html', context={'message': "上传数据用于画像建模"})

    def post(self, request):
        global file_name
        try:
            media_file = request.FILES.get('media_file')
            file_name = media_file.name
            if (file_name.split('.')[1] != 'csv') and (file_name.split('.')[1] != 'xlsx'):
                return render(request, 'training/training-upload.html', context={'message': '格式错误'})
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            # 写入文件
            with open(file_path, 'wb+') as f:
                for chunk in media_file.chunks():
                    f.write(chunk)

            print(f'上传成功！文件保存在：{file_path}')
            # return redirect('training:execute_training')
            return render(request, 'training/training-upload.html', context={'message': f'上传成功！'})
        except Exception as e:
            print(e)
            return render(request, 'training/training-upload.html', context={'message': '上传出错，请重新上传'})


# 执行情感分析
class SentimentAnalysis(View):

    def get(self, request):
        # 导入数据集
        data = pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'data.xlsx'), sheet_name='Sheet1')
        y = data['情感分析']

        # 遍历整张表格，对所有评论进行分词
        words = []
        for comm in data['评价'].tolist():
            word = jieba.cut(comm)
            result = ' '.join(word)
            words.append(result)

        # 文本向量化
        vect = CountVectorizer()
        X = vect.fit_transform(words)
        X = X.toarray()

        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)

        # 定义多层感知机MLP分类器
        mlp = MLPClassifier(hidden_layer_sizes=(64, 64, 32))

        # 拟合模型
        mlp.fit(X_train, y_train)

        # 保存mlp模型
        model_path = os.path.join(settings.STATICFILES_DIRS[0], 'model/mlp_model.pkl')
        joblib.dump(mlp, model_path)

        return render(request, 'training/training-visualization.html', context={'msg': '情感分析建模已完成！'})


# 展示数据集
def display_dataset(request):
    # 导入数据集
    data = pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'data.xlsx'), sheet_name='Sheet1')
    print(data)
    # 设置每页显示的数量
    paginator = Paginator(data, per_page=10)  # 每页显示10篇文章

    # 获取当前请求页面的页码，默认为1
    page_number = request.GET.get('page', 1)

    # 尝试获取指定页码的数据
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # 如果请求的页码不是整数，则返回第一页
        page_obj = paginator.page(1)
    except EmptyPage:
        # 如果请求的页码超出范围，则返回最后一页
        page_obj = paginator.page(paginator.num_pages)

    context = {'page_obj': page_obj}

    return render(request, 'training/training-display-dataset.html', context=context)
