from django.shortcuts import render, redirect, reverse
from django.views import View
from user.models import User
# Create your views here.


class Login(View):

    def get(self, request):
        # 判断一下是否有cookie
        user_login = request.COOKIES.get('user_login')
        if user_login == 'is_login':
            return redirect('user:user_portrait')  # 如果有cookie就直接进来
        else:
            # 登录页
            return render(request, 'login/page-login.html')

    def post(self, request):
        try:
            username = request.POST.get('username')
            print(username)
            user = User.objects.get(name=username)

            if not user:
                return render(request, 'login/page-login.html', context={'msg': '账号密码错误'})
            else:
                password = request.POST.get('password')
                print(username, password)
                if (username == user.name) and (password == user.password):
                    response = render(request, 'user/user-upload.html')
                    response.set_cookie("user_login", "is_login")
                    response.set_cookie("username", user.name)
                    print(username)
                    return response
                else:
                    return render(request, 'login/page-login.html', context={'msg': '账号密码错误'})
        except Exception as e:
            print(e)
            return render(request, 'login/page-login.html', context={'msg': '账号密码错误'})


# 退出登录
def logout(request):
    user_login = request.COOKIES.get('user_login')
    print('logout = ', user_login)
    if user_login == 'is_login':
        response = render(request, 'login/page-login.html')
        response.delete_cookie('user_login')
        response.delete_cookie('username')
        return response
    else:
        return render(request, 'user/user-upload.html')
