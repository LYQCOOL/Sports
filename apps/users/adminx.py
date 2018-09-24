# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/23 20:53'
import xadmin

from .models import UserProfile,VerifyCode
from xadmin import views
from excersise.models import Sports
from schools.models import Schools


class GlobalSetting(object):
    # 页头
    site_title = '悦动乐后台管理系统'
    # 页脚
    site_footer = '悦动乐'
    # 左侧样式
    menu_style = 'accordion'
    # 设置models的全局图标
    global_search_models = [UserProfile, Sports]
    global_models_icon = {
        UserProfile: "glyphicon glyphicon-user", Sports: "fa fa-cloud",Schools:"fa fa-xing"
    }


class BaseSetting(object):
    '''
    主题样式多样化
    '''
    enable_themes = True
    use_bootswatch = True


class VerifyCodeAdmin(object):
    list_display=['code','mobile','add_time']
    search_fields=['code','mobile']
    list_filter=['code','mobile']

xadmin.site.register(VerifyCode,VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
