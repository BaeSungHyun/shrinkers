from django.contrib import messages
from shortener.forms import UrlCreateForm
from django.shortcuts import redirect, render, get_object_or_404
from shortener.models import ShortenedUrls
from django.contrib.auth.decorators import login_required
from shortener.utils import url_count_charger


def url_redirect(request, prefix, url):
    print(prefix, url)
    get_url = get_object_or_404(ShortenedUrls, prefix=prefix, shortend_url=url)
    is_permanent = False
    target = get_url.target_url
    if get_url.creator.organization:  # Premium
        is_permanent = True  # 301

    if not target.startswith("https://") and not target.startswith("https://"):
        target = "https://" + get_url.target_url

    return redirect(target, permanent=is_permanent)


def url_list(request):
    get_list = ShortenedUrls.objects.order_by("-created_at").all()
    return render(request, "url_list.html", {"list": get_list})


@login_required
def url_create(request):
    msg = None
    if request.method == "POST":
        form = UrlCreateForm(request.POST)
        if form.is_valid():
            msg = (
                f"{form.cleaned_data.get('nickname')} 생성 완료!"  # cleaned_data 받으려고 f 붙임
            )
            messages.add_message(request, messages.INFO, msg)
            form.save(request)  # why need request?
            return redirect("url_list")
        else:
            form = UrlCreateForm()
    else:
        form = UrlCreateForm()
    return render(request, "url_create.html", {"form": form})


@login_required
def url_change(request, action, url_id):  # url_id from urls.py
    if request.method == "POST":
        url_data = ShortenedUrls.objects.filter(id=url_id)
        if url_data.exists():
            if url_data.first().creator_id != request.user.id:
                msg = "자신이 소유하지 않은 URL 입니다"
            else:
                if action == "delete":
                    msg = f"{url_data.first().nick_name} 삭제 완료!"
                    try:
                        url_data.delete()
                    except Exception as e:
                        print(e)
                    else:
                        url_count_charger(request, False)
                    messages.add_message(request, messages.INFO, msg)
                elif action == "update":
                    msg = f"{url_data.first().nick_name} 수정 완료!"
                    form = UrlCreateForm(request.POST)
                    form.update_form(request, url_id)

                    messages.add_message(request, messages.INFO, msg)
        else:
            msg = "해당 URL 정보를 찾을 수 없습니다."
    elif request.method == "GET" and action == "update":
        url_data = ShortenedUrls.objects.filter(pk=url_id).first()
        form = UrlCreateForm(instance=url_data)  # add existing url_data into form
        return render(request, "url_create.html", {"form": form, "is_update": True})

    return redirect("url_list")
