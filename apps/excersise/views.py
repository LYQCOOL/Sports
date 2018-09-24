from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .serializers import *
from .models import *
from .filter import SportsFilter
from utils.permissions import IsOwnerOrReadOnly


# Create your views here.


class SchdulePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class SportsViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
         显示所有运动列表
    retrieve:
         运动详情
    '''
    serializer_class = SportsSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    pagination_class = SchdulePagination

    def get_queryset(self):
        return Sports.objects.filter(school=self.request.user.school)


class ScheduleViewset(viewsets.ModelViewSet):
    '''
    list:
      列出所有本校的发起约运动列表
    retrieve:
      查看约运动详情
    update:
      修改自己发起的约运动信息
    delete:
      删除自己发起的约运动
    '''
    serializer_class = ScheduleSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    pagination_class = SchdulePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = SportsFilter
    search_fields = ('user__name', 'sport__sport_name')
    ordering_fields = ('sport_time',)

    def get_queryset(self):
        if self.action == 'list' or self.action == 'retrieve':
            return Schedule.objects.all()
        else:
            return Schedule.objects.filter(school=self.request.user.school)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScheduleDetailSerializer
        elif self.action == 'create':
            return ScheduleSerializer
        elif self.action == 'list':
            return ScheduleListSerializer
        return ScheduleSerializer

        # def perform_create(self, serializer):
        #      obj=serializer.save()
        #      obj.school=UserProfile.objects.filter(user=self.request.user).school
        #      obj.save()
        #      return obj


class JoinScheduleViewset(mixins.ListModelMixin, mixins.DestroyModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    约运动功能
    加入约运动
    list:
        列出所有发起的约运动
    retrieve:
        查看约运动的详情
    create:
        发起约运动
    destroy:
        删除约运动

    '''
    queryset = JoinSchedule.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return MyJoinScheduleDetailSerializer
        elif self.action == 'create':
            return MyJoinScheduleSerializer
        return MyJoinScheduleSerializer


class FavViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        列出所有我喜欢的运动
    retrieve:
        查看我喜欢的运动详情
    create:
        添加我喜欢的运动
    destroy:
        删除我喜欢的运动
    '''
    serializer_class = FavSportsSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Sport_Fav.objects.filter(student=self.request.user)
