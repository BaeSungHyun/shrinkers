from shortener.models import ShortenedUrls, Users
from shortener.urls.serializers import UserSerializer, UrlListSerializer
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = ShortenedUrls.objects.all().order_by("-created_at")
    serializer_class = UrlListSerializer
    # 로그인 된 유저만 api 사용 가능
    permission_classes = [permissions.IsAuthenticated]