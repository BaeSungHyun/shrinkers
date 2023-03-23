from typing import List
from shortener.schemas import Users as U
from shortener.schemas import TelegramUpdateSchema
from shortener.models import Users
from ninja.router import Router

user = Router()

@user.get("", response=List[U]) # decorator로 endpoint 지정
def get_user(request):
    a = Users.objects.all() # 실제로 현업에서는 filter같은 것을 쓴다
    return list(a)

@user.post("", response={201: None})
def update_telegram_username(request, body: TelegramUpdateSchema):
    user = Users.objects.filter(user_id = request.user.id)
    if not user.exists():
        return 404, {"msg":"No user found"}
    user.update(telegram_username = body.username)
    return 201, None