from ninja.router import Router
from shortener.models import Users
from shortener.schemas import Users as U
from typing import List


user = Router()


@user.get("", response=List[U])
def get_user(request):
    a = Users.objects.all()
    return list(a)