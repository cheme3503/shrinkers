from shortener.utils import MsgOk, url_count_changer
from rest_framework.decorators import renderer_classes, action
from shortener.models import Users, ShortenedUrls
from shortener.urls.serializers import *
from django.http.response import Http404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

class UrlListView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = ShortenedUrls.objects.order_by("-created_at")
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        #POST METHOD
        serializer = UrlCreateSerializer(data=request.data)
        # print(serializer.is_valid())
        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            return Response(UrlListSerializer(rtn).data, status=status.HTTP_201_CREATED)
        pass

    def retrieve(self, request, pk=None):
        # Detail GET
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
    def destroy(self, request, pk=None):
        #Delete Method
        queryset = self.get_queryset().filter(pk=pk, creator_id = request.user.id)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        url_count_changer(request, False)
        return MsgOk()

    def list(self, request):
        queryset=self.get_queryset().all()
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get','post'])
    def add_click(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id = request.user.id)
        if not queryset.exists():
            raise Http404
        rtn = queryset.first().clicked()
        serializer = UrlListSerializer(rtn)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def remove_click(self, request, pk=None):
        print("remove")


