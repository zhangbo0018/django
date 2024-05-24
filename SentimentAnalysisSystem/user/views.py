from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
import joblib
import jieba
import parsel
import numpy as np
import os
import requests
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from django.conf import settings
from math import floor
from django.utils import timezone
from user.models import User, UserCategoryAffinity
from wordcloud import WordCloud
import jieba

# Create user views here.
r_count = 0
product_detail = []
accuracy = 0
interest_preference = pd.Series()
comment = []
goods_types = []

def display_user(request):

    return HttpResponse('ok')


class UserPortrait(View):

    def get(self, request):
        context = {
            'message': '上传数据开始用户画像'
        }
        return render(request, 'user/user-upload.html', context=context)


    def post(self, request):
        try:
            # 一、读取数据
            media_file = request.FILES.get('media_file')
            file_name = media_file.name
            if file_name.split('.')[1] != 'xlsx':
                return render(request, 'user/user-upload.html', context={'message': '格式错误'})
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            if not os.path.exists(file_path):
                return render(request, 'user/user-upload.html', context={'message': '您尚未进行用户画像建模'})

            # 二、情感分析
            # 加载模型
            mlp = joblib.load(os.path.join(settings.STATICFILES_DIRS[0], 'model/mlp_model.pkl'))
            # 导入数据集
            data = pd.read_excel(file_path, sheet_name='Sheet1')
            y = data['情感分析']
            global comment
            comment = data['评价'].tolist()

            # 遍历整张表格，对所有评论进行分词
            words = []
            for comm in data['评价'].tolist():
                word = jieba.cut(comm)
                result = ' '.join(word)
                words.append(result)

            # 文本向量化
            vect = CountVectorizer()
            X = vect.fit_transform(words)
            X_test = X.toarray()

            y_pred = mlp.predict(X_test)
            y_pred = np.array(y_pred)
            # 计算True的比例
            global accuracy
            global interest_preference
            accuracy = np.mean(y_pred == y)
            accuracy = np.round(accuracy, 2)

            # 三、基于情感分析提取用户兴趣偏好特征提取（画像）
            # 按'商品品类'进行分组，对'情感分析'字段中的1进行计数并计算占比（即兴趣偏好）
            interest_preference = data.groupby('商品品类')['情感分析'].apply(lambda x: (x == 1).sum() / len(x))

            # 保存用户画像数据到数据库
            username = request.COOKIES.get('username')
            user = User.objects.get(name=username)
            for CategoryAffinity in interest_preference.to_dict().items():
                UserCategoryAffinity.objects.create(
                    user=user,
                    category_name=CategoryAffinity[0],
                    affinity_score=CategoryAffinity[1],
                    update_time=timezone.now()
                )
            return render(request, 'user/user-upload.html', context={'message': '用户画像成功'})

        except Exception as e:
            print(e)
            return render(request, 'user/user-upload.html', context={'message': '用户画像失败'})


class UserRegister(View):
    def get(self, request):

        return render(request, 'user/user-register.html')

    def post(self, request):
        # 一、读取数据
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        create_time = timezone.now()
        User.objects.create(name=username, gender=gender, password=password, create_time=create_time)
        print(username, gender, password, create_time)

        # 返回响应
        return render(request, 'login/page-login.html')


class PersonalizedRecommendation(View):

    def get(self, request):
        # 一、读取数据
        username = request.COOKIES.get('username')
        user = User.objects.get(name=username)
        # 通过user对象获取所有相关的UserCategoryAffinity条目
        category_affinities = user.usercategoryaffinity_set.all()
        # 现在category_affinities是一个QuerySet，包含所有与用户相关的UserCategoryAffinity对象
        dct = {}
        for affinity in category_affinities:
            # 总是获取最新的商品品类兴趣度
            dct[affinity.category_name] = affinity.affinity_score

        interest_preference = pd.DataFrame.from_dict(dct, orient='index', columns=['相关度'])
        interest_preference.rename_axis('类别').reset_index(inplace=True)

        # 二、基于兴趣偏好特征的推荐算法
        # 兴趣偏好归一化处理
        # 计算最高和最低好感值
        max_val = interest_preference.max()
        min_val = interest_preference.min()
        # 计算归一化后的好感值占比
        normalized_values = (interest_preference - min_val) / (max_val - min_val)
        # 初始分配的商品数量
        allocated_counts = normalized_values * 9
        # 对分配结果进行四舍五入取整
        rounded_counts = np.round(allocated_counts, 0)
        # 推荐列表处理，防止某一推荐商品数量比重过大
        rounded_counts[rounded_counts > 5] = 3
        rounded_counts['相关度'].astype(int)
        rounded_counts = rounded_counts['相关度'].to_dict()
        global goods_types
        goods_types = list(rounded_counts.keys())

        # 三、爬取商品信息
        if user.gender:
            gender = '男'
        else:
            gender = '女'

        global r_count
        global product_detail

        for product_item in rounded_counts.items():
            print('product_item', product_item)
            if r_count > 8:
                break

            spider = ProductCrawler(product_item[0], int(product_item[1]), gender)
            spider.run()

        r_count = 0  # 重置计数器

        # 返回响应
        context = {
            'product_detail': product_detail,
        }
        product_detail = []
        return render(request, 'user/user-recommend.html', context=context)


class ProductCrawler:

    def __init__(self, product, count, gender):
        self.product = product
        self.headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': '_snmc=1; _snsr=bing.com%7Creferral%7C%7C%7C; _snvd=1707015075806C8Bz2BMhxPU; _snzwt=THcoa918d720700c1QvzZ80ba; SN_CITY=160_736_1000156_9156_01_11238_2_0; cityCode=736; districtId=11238; streetCode=7360199; ssotbrd=TGTynjsF1imhi8XLKKGjtW0eXKJrKipMPqJ17qIAgG0; authId=siKGOZbK2BKGG3CnjqJCExoBl1RleWrM9d; secureToken=A1B2898B7F6FD45E781086F3B503E9CB; tradeMA=47; cityId=9156; totalProdQty=0; hm_guid=99cebc76-4c20-4738-b758-c4690dd2dda3; _df_ud=ba506502-9e81-47de-b38a-6b04207b22a5; sesab=ACBACBEBBAEABB; sesabv=24%2C12%2C9%2C1%2C28%2C8%2C4%2C20%2C4%2C4%2C8%2C1%2C1%2C2; _snms=170701531857413199; _snma=1%7C170701507704025216%7C1707015077040%7C1707015318538%7C1707015412973%7C7%7C1; _snmp=170701541210297525; _snmb=170701507721495249%7C1707015413008%7C1707015412975%7C7; ariaDefaultTheme=undefined; token=7cafb339-1843-4f0a-acbe-a46de04f95eb; _snck=170701542001941805',
            'Referer': 'https://www.suning.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        }
        self.cookie = {}
        self.user_gender = gender
        self.url = f'https://search.suning.com/{product}{gender}/'
        self.html = ''
        self.count = count

    def get_data(self):

        try:
            response = requests.get(url=self.url, headers=self.headers)
            response.encoding = 'utf-8'
            self.html = response.text
        except Exception as e:
            print(e)
            pass

    def parse_data(self):

        global r_count
        global product_detail
        selector = parsel.Selector(text=self.html)
        for i in range(0, self.count):
            if r_count > 8:
                break
            # 获得商品图片
            src = selector.css('ul.general li')[i].css('img::attr(src)').get()
            src = 'https:' + src
            # 获得商品描述
            title = selector.css('ul.general li')[i].css('img::attr(alt)').get()
            print(src, title)
            product_detail.append({'src': src, 'title': title})

            r_count += 1

    def run(self):
        self.get_data()
        self.parse_data()


def display_recommend(request):
    global product_detail
    if product_detail:
        return render(request, 'user/user-recommend.html', context={'product_detail': product_detail})
    else:
        return render(request, 'user/user-upload.html', context={'message': '请先进行用户画像'})


def visualization(request):

    global interest_preference
    global comment

    user = User.objects.get(name=request.COOKIES.get('username'))
    if not interest_preference.empty:
        # 获取索引
        index = interest_preference.index.tolist()
        # 获取相关的兴趣度
        affinity = interest_preference.tolist()
        # 变成字典
        data = interest_preference.to_dict()
        print(index, affinity)
        # 构建词云
        # 导入数据集
        # 遍历整张表格，对所有评论进行分词
        text = " ".join(comment)
        print(text)
        # 首先进行分词
        word_list = jieba.lcut(text)
        # 在用空格将分词拼成字符串
        text_new = ' '.join(word_list)
        # 实例化词云对象
        wc = WordCloud(
            width=800,
            height=400,
            background_color='white',
            font_path=os.path.join(settings.STATICFILES_DIRS[0], 'font/MSYH.TTF')
        )  # 要指定字体
        # 生成词云图
        wc.generate(text_new)
        # 保存词云图
        wc.to_file(os.path.join(settings.MEDIA_ROOT, 'wordcloud.jpg'))

    else:
        return redirect('user:user_portrait')

    context = {
        'username': user.name,
        'accuracy': accuracy,
        'index': index,
        'affinity': affinity,
        'data': data,
    }
    return render(request, 'user/user-visualization.html', context=context)


class RecommendationFeedback(View):

    def get(self, request):
        context = {
            "goods_types": goods_types
        }
        return render(request, 'user/user-recommend-feedback.html', context=context)

    def post(self, request):
        pass
