from django.shortcuts import render, redirect, reverse
from django.views import View
# Create your views here.


class login(View):

    def get(self, request):
        # 判断一下是否有cookie
        user = request.COOKIES.get('user')
        print(user)
        if user == 'is_login':
            return render(request, 'index.html')  # 如果有cookie就直接进来
        else:
            # 重定向到登录页
            return render(request, 'login/page-login.html')

    def post(self, request):
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == 'admin' and pwd == 'admin':
            response = render(request, 'index.html')
            response.set_cookie("user", "is_login")  # 登录成功写cookie
            return response
        else:
            return render(request, 'login/page-login.html', context={'msg': '账号密码错误'})


# 退出登录
def logout(request):
    user = request.COOKIES.get('user')
    print('logout = ', user)
    if user == 'is_login':
        response = redirect('login:login')
        response.delete_cookie('user')
        return response
    else:
        return redirect('login:login')
