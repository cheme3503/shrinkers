from ninja.router import Router
from shortener.models import Users
from shortener.schemas import Users as U
from typing import List
from shortener.schemas import TelegramUpdateSchema


user = Router()


@user.get("", response=List[U])
def get_user(request):
    a = Users.objects.all()
    return list(a)
@user.post("", response={201: None})
def update_telegram_username(request, body: TelegramUpdateSchema):
    user = Users.objects.filter(user_id=request.user.id)
    if not user.exists():
        return 404, {"msg": "No user found"}
    user.update(telegram_username = body.username)
    return 201, None