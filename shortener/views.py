from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shortener.models import Users, ShortenedUrls
from shortener.forms import RegisterForm, LoginForm, UrlCreateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


# Inside 'request', 'User' table data gets in
def index(request):
    return render(request, "base.html", {"welcome_msg": f"Hello"})


def redirect_test(request):
    print("Go redirect")
    return redirect("index")  # urls.py name="index"


# When we use jsrf token (json token), we don't need csrf token in django
@csrf_exempt  # disables CSRF protection. POST method always requires csrf token.
def get_user(request, user_id):  # 'user_id' from urls.py <int:user_id>
    print(user_id)
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first()  # parameter 'user_id'
        # query string으로 넘겼지만 body, header  등으로 다양하게 넘길 수 있다
        return render(request, "base.html", {"user": user, "params": [abc, xyz]})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)
        # POST : single-page application 에서 뒤에서 비동기로 요청하고 json 으로 받아와서 dom update
        return JsonResponse(
            status=201, data=dict(msg="You just reached with Post Method!")
        )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "Incorrect Data"
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "Resiter Completed"
        return render(request, "register.html", {"form": form, "msg": msg})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


def login_view(request):
    is_ok = False
    if request.method == "POST":
        print(
            request.POST
        )  # <QueryDict: {'csrfmiddlewaretoken': ['TELoePZlgAIvqvV1RtAmRRWncM4MiyAr2TVoCoIDbC2kOswzYMn3JC2EvYb5107M'], 'username': ['gai'], 'password': ['0420']}>
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
                user = Users.objects.get(
                    user__email=email
                )  # __ : go to ForeignKey path and search in another table
            except (
                Users.DoesNotExist
            ):  # If above does not have Users, DoesNotExist error occurs. Prevent it!
                pass
            else:  # if it doesn't go to except, then else performs
                if user.user.check_password(raw_password):  # return boolean value.
                    # check_password only works in django's auth user table. user.user returns mapped object.
                    msg = None
                    login(request, user.user)
                    is_ok = True
                    # request 가 Middleware을 지나오면서 session data를 담고 있음. dict 형태. key는 항상 string!
                    request.session[
                        "remember_me"
                    ] = remember_me  # Save it in session. in dict form

                    # if not remember_me" 크롬에서는 잘 안되더라. 장고 권유 방법이긴 함.
                    #   request.session.set_expiry(0) 브라우저를 닫았을 때 자동으로 세션 종료.

    else:  # GET request
        msg = None
        form = LoginForm()
    # print("REMEMBER ME: ", request.session.get("remember_me")) # False or True
    return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})

    # else:
    #     form = AuthenticationForm()

    # for visible in form.visible_fields():
    #     print(form.visible_fields()) # only two. Username and Password
    #     visible.field.widget.attrs["placeholder"] = "유저ID" if visible.name == "username" else "패스워드"
    #     visible.field.widget.attrs["class"] = "form-control"
    return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})


def logout_view(request):
    logout(request)
    return redirect("index")  # urls.py name="index"


@login_required
def list_view(request):
    page = int(request.GET.get("p", 1))  # if p does not exist : 1
    print(request.GET)  # <QueryDict: {'p': ['2']}>
    users = Users.objects.all().order_by("-id")  # ORM
    paginator = Paginator(users, 10)  # 10 users per each page
    print(paginator)  # <django.core.paginator.Paginator object at 0x000001C926623130>
    users = paginator.get_page(page)  # input 10 users in page. returns page
    print(users)  # <Page 2 of 6>
    return render(request, "boards.html", {"users": users})
