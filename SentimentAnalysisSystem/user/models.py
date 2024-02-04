from django.db import models

# Create user models here.


# 定义用户模型类
class User(models.Model):

    # 用户id
    id = models.AutoField(unique=True, primary_key=True, auto_created=True)
    # 用户姓名
    name = models.CharField(max_length=100)
    # 用户性别
    gender = models.BooleanField(default=1)  # 默认是1，表示男
    # 用户密码
    password = models.CharField(max_length=100)
    # 用户权限
    is_admin = models.BooleanField(default=0)  # 默认是0，表示普通用户
    # 用户画像创建
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_user'
        verbose_name = '用户'


# 定义基于情感分析的用户画像模型类
class UserCategoryAffinity(models.Model):

    # 用户画像id
    id = models.AutoField(unique=True, primary_key=True, auto_created=True)
    # 关联的用户user_id，关联用户表
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # 类别名称
    category_name = models.CharField(max_length=100)
    # 兴趣偏好得分
    affinity_score = models.FloatField()
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_category_affinity'
        verbose_name = '用户画像'
