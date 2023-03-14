from shortener.models import ShortenedUrls, Users
from django.db.models import (
    F,
)  # An object capable of resolving references to existing query objects.


def url_count_charger(request, is_increase: bool):
    count_number = 1 if is_increase else -1

    Users.objects.filter(
        user_id=request.user.id
    ).update(  # shortener_user, auth_user  2개!
        url_count=F("url_count") + count_number
    )
