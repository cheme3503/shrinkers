from shortener.utils import MsgOk, get_kst, url_count_changer
from rest_framework.decorators import renderer_classes, action
from shortener.models import ShortenedUrls, Statistic, Users
from shortener.urls.serializers import *
from django.http.response import Http404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from datetime import timedelta
from django.db.models.aggregates import Count, Min
from django.core.cache import cache

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
        queryset= cache.get('url_list')
        if not queryset:
            queryset = self.get_queryset().filter(creator_id = request.user.id).all()
            cache.set('url_list', queryset, 20)

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

    @action(detail=True, methods=["get", "post"])
    def add_browser_today(self, request, pk=None):
        queryset = self.get_queryset().filter(pk=pk, creator_id=request.user.id).first()
        new_history = Statistic()
        new_history.record(request, queryset, {})
        return MsgOk()
    #
    @action(detail=True, methods=["get"])
    def get_browser_stats(self, request, pk=None):
        queryset = Statistic.objects.filter(
            shortened_url_id=pk,
            shortened_url__creator_id=request.user.id,
            created_at__gte=get_kst() - timedelta(days=14),
        )
        if not queryset.exists():
            raise Http404

        browers = (
            queryset.values("web_browser")
            .annotate(count=Count("id"))
            .values("count", "web_browser")
            .order_by("-count")
        )
        serializer = BrowerStatSerializer(browers, many=True)
        return Response(serializer.data)


