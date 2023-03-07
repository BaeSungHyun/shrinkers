from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shortener.models import Users, ShortenerUrls
from shortener.forms import RegisterForm, LoginForm, UrlCreateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

# Inside 'request', 'User' table data gets in
def index(request):
    print(request.user) # __repr__ : request.user.username
    # print(request.user.pay_plan)
    print(request.user.id)
    print(request.user.is_superuser)
    user = Users.objects.filter(id=request.user.id).first() # able to get 0,1,2...
    # user = Users.objects.get(username="Gai") # able to get only 1! Else error! Used for validation
    email = user.email if user else "Anonoymous User!"
    print(email)
    print(request.user.is_authenticated)
    if not(request.user.is_authenticated):
        email = "Anonymous User!" 
        print(email)
    return render(request, "base.html", {"welcome_msg": f"Hello {email}"})


def redirect_test(request):
    print("Go redirect")
    return redirect("index") # urls.py name="index"

# When we use jsrf token (json token), we don't need csrf token in django
@csrf_exempt # disables CSRF protection. POST method always requires csrf token.
def get_user(request, user_id): # 'user_id' from urls.py <int:user_id>
    print(user_id)
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first() # parameter 'user_id'
        # query string으로 넘겼지만 body, header  등으로 다양하게 넘길 수 있다
        return render(request, "base.html", {"user": user, "params":[abc, xyz]})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)
        # POST : single-page application 에서 뒤에서 비동기로 요청하고 json 으로 받아와서 dom update
        return JsonResponse(status=201, data= dict(msg="You just reached with Post Method!"))

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "Incorrect Data"
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "Resiter Completed"
        return render(request, "register.html", {"form":form, "msg":msg})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form":form})

def login_view(request):
    is_ok = False
    if request.method == "POST":
        print(request.POST) # <QueryDict: {'csrfmiddlewaretoken': ['TELoePZlgAIvqvV1RtAmRRWncM4MiyAr2TVoCoIDbC2kOswzYMn3JC2EvYb5107M'], 'username': ['gai'], 'password': ['0420']}>
        # form = AuthenticationForm(request, request.POST) # 우리가 만든 form 이 아니라 only username, password 
        form = LoginForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
        #     user = authenticate(username=username, password=raw_password) # returns a User object
        #     if user is not None:
        #         login(request, user)
        #         is_ok = True
        # else: 
            remember_me = form.cleaned_data.get("remember_me")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                user = Users.objects.get(email=email) 
            except Users.DoesNotExist: # If above does not have Users, DoesNotExist error occurs. Prevent it!
                pass
            else: # if it doesn't go to except, then else performs
                if user.check_password(raw_password): # return boolean value
                    msg = None
                    login(request, user)
                    is_ok = True
                    # request 가 Middleware을 지나오면서 session data를 담고 있음. dict 형태. key는 항상 string!
                    request.session["remember_me"] = remember_me # Save it in session. in dict form

                    # if not remember_me" 크롬에서는 잘 안되더라. 장고 권유 방법이긴 함.
                    #   request.session.set_expiry(0) 브라우저를 닫았을 때 자동으로 세션 종료.

    else: # GET request
        msg = None 
        form = LoginForm()
    print("REMEMBER ME: ", request.session.get("remember_me")) # False or True
    return render(request, "login.html", {"form":form, "msg":msg, "is_ok":is_ok})


    # else:
    #     form = AuthenticationForm()

    # for visible in form.visible_fields():
    #     print(form.visible_fields()) # only two. Username and Password
    #     visible.field.widget.attrs["placeholder"] = "유저ID" if visible.name == "username" else "패스워드"
    #     visible.field.widget.attrs["class"] = "form-control" 
    return render(request, "login.html", {"form": form, "msg": msg, "is_ok":is_ok})

def logout_view(request):
    logout(request)
    return redirect("index") # urls.py name="index"

@login_required
def list_view(request):
    page = int(request.GET.get("p",1)) # if p does not exist : 1
    print(request.GET) # <QueryDict: {'p': ['2']}>
    users = Users.objects.all().order_by('-id') # ORM
    paginator = Paginator(users, 10) # 10 users per each page
    print(paginator) # <django.core.paginator.Paginator object at 0x000001C926623130>
    users = paginator.get_page(page) # input 10 users in page. returns page
    print(users) # <Page 2 of 6>
    return render(request, "boards.html", {"users":users})


def url_list(request):
    get_list = ShortenerUrls.objects.order_by("-created_at").all()
    return render(request, "url_list.html", {"list":get_list})


@login_required
def url_create(request):
    msg = None
    if request.method == "POST":
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            msg = f"{form.cleaned_data.get('nick_name')} 생성 완료!"
            messages.add_message(request, messages.INFO, msg) # add message into reqeust
            form.save(request)
            return redirect("url_list") # urls.py name="url_list"
        else:
            form = UrlCreateForm()
    else: 
        form = UrlCreateForm()
    return render(request, "url_create.html", {"form":form})

@login_required
def url_change(request, action, url_id):
    if request.method == "POST":
        url_data = ShortenerUrls.objects.filter(pk=url_id)
        if url_data.exists():
            if url_data.first().created_by_id != request.user.id:
                msg = "자신이 소유하지 않은 URL 입니다."
            else:
                if action == "delete":
                    msg = f"{url_data.first().nick_name} 삭제 완료!"
                    url_data.delete()
                    messages.add_message(request, messages.INFO, msg)
                elif action == "update":
                    msg = f"{url_data.first().nick_name} 수정 완료!"
                    form = UrlCreateForm(request.POST)
                    form.update_form(request, url_id)

                    messages.add_message(request, messages.INFO, msg)

        else:
            msg = "해당 URL 정보를 찾을 수 없습니다."
    elif request.method == "GET" and action == "update":
        url_data = ShortenerUrls.objects.filter(pk=url_id).first()
        form = UrlCreateForm(instance = url_data)
        return render(request, "url_create.html", {"form": form, "is_update":True})
    
    return redirect("url_list")
                    
        
