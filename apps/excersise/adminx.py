# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/23 20:53'
import xadmin

from .models import *


class SportsAdmin(object):
    list_display = ['school','sport_name', 'image', 'add_time']
    search_fields = ['school','sport_name', 'image']
    list_filter = ['school','sport_name', 'image', 'add_time']
    ordering=['school','sport_name']


class Sport_FavAdmin(object):
    list_display = ['student', 'sport', 'add_time']
    search_fields = ['student', 'sport']
    list_filter = ['student__username', 'sport__sport_name', 'add_time']


class ScheduleAdmin(object):
    list_display = ['status','school','user', 'sport', 'sport_time', 'people_nums', 'now_people']
    search_fields = ['status','school','user', 'sport', 'sport_time', 'people_nums', 'now_people']
    list_filter = ['status','school','user', 'sport', 'sport_time', 'people_nums', 'add_time', 'now_people']
    # 导出类型
    list_export = ('xls', 'xml', 'json')
    # 导出字段
    list_export_fields = ('user', 'sport', 'sport_time')
    ordering=['school','sport','user']


class JoinScheduleAdmin(object):
    list_display = ['schedule', 'user', 'add_time']
    search_fields = ['schedule', 'user']
    list_filter = ['schedule','schedule__sport', 'user__school', 'user','add_time']


xadmin.site.register(Sports, SportsAdmin)
xadmin.site.register(Sport_Fav, Sport_FavAdmin)
xadmin.site.register(Schedule, ScheduleAdmin)
xadmin.site.register(JoinSchedule,JoinScheduleAdmin)
