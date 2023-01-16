from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shortener.forms import RegisterForm, LoginForm, UrlCreateForm
from shortener.models import *
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, "base.html", {"welcome_msg":'Hello FastCampus!'})

@csrf_exempt
def get_user(request, user_id):
    print(user_id)
    if request.method == 'GET':
        abc = request.GET.get('abc')
        xyz = request.GET.get('xyz')
        user = Users.objects.filter(pk=user_id).first()
        return render(request, 'base.html', {'user':user, 'params': [abc, xyz]})

    elif request.method =="POST":
        username = request.GET.get('username')
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)

        return JsonResponse(dict(msg='You just reached with Post Method'))

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) #authenticate method : User instance를 return
            login(request, user) # signs in session 생성
            msg = "회원가입완료"

        return render(request, "register.html", {"form":form, "msg":msg})

    else:
        form = RegisterForm()
        return render(request, "register.html", {})

def login_view(request):
    is_ok = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get("remember_me")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                user = Users.objects.get(user__email=email)
            except Users.DoesNotExist:
                pass

            else:
                if user.user.check_password(raw_password):  #비교를 함에 있어 password hashing을 고려하여, 주어진 string이 user의 올바른 password이면 True 값을 반환함.
                    msg= None
                    login(request, user.user)
                    is_ok = True
                    request.session["remember_me"] = remember_me
                    return redirect('index')

    else:
        msg=None
        form=LoginForm()
        if request.user.is_authenticated:
            return redirect('index')

    # print("REMEMBER_ME: ", request.session.get("remember_me"))

    return render(request, 'login.html', {'form':form, 'msg':msg, 'is_ok':is_ok})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def list_view(request):
    page = int(request.GET.get('p',1))        #default 로 1 값을 가짐
    users = Users.objects.all().order_by('-id')
    paginator = Paginator(users, 1)            #django.core.paginator.Paginator class 는 pagination sequence를 생성하는 class임.
    users = paginator.get_page(page)  #Paginator.get_page(number) method 는 1 값을 기본으로 하는 Page 객체를 반환함.

    return  render(request, 'boards.html', {'users':users})