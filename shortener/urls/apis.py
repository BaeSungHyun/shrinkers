from shortener.models import ShortenedUrls, Users
from shortener.urls.serializers import UserSerializer, UrlListSerializer, UrlCreateSerializer
from django.contrib.auth.models import User, Group
from rest_framework.decorators import renderer_classes, action
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from shortener.utils import MsgOk, url_count_charger
from shortener.urls import serializers
from django.http.response import Http404

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = ShortenedUrls.objects.order_by("-created_at")
    serializer_class = UrlListSerializer
    # 로그인 된 유저만 api 사용 가능
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        # POST METHOD
        serializer = UrlCreateSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            return Response(UrlListSerializer(rtn).data, status=status.HTTP_201_CREATED)
        pass

    def retrieve(self, request, pk=None):
        # DETAIL GET
        queryset = self.get_queryset().filter(pk=pk).first()
        serializer = UrlListSerializer(queryset)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        # PUT METHOD
        pass

    def partial_update(self, request, pk=None):
        # PATCH METHOD
        pass

    @renderer_classes([JSONRenderer])
    def delete(self, request, pk=None):
        # DELETE METHOD
        queryset = self.get_queryset().filter(pk=pk, creator_id = request.user.id)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        url_count_charger(request, False)
        return MsgOk()

    def list(self, request):
        # GET ALL
        queryset = self.get_queryset().all()
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"])
    def add_click(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id)
        if not queryset.exists():
            raise Http404
        rtn = queryset.first().clicked()
        serializer = UrlListSerializer(rtn)
        return Response(serializer.data)