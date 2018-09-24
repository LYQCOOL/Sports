"""Sports URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import xadmin
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from excersise.views import SportsViewset, ScheduleViewset, JoinScheduleViewset, FavViewset
from schools.views import SchoolViewset
from users.views import SmsCodeViewset, UserViewset, SmsCodeViewset
from Sports.settings import MEDIA_ROOT

router = DefaultRouter()
# 配置短信验证接口
router.register(r'codes', SmsCodeViewset, base_name='codes')
# 配置运动相关url
router.register(r'sports', SportsViewset, base_name='sports')
# 配置与学校相关url
router.register(r'schools', SchoolViewset, base_name='schools')
# 配置users验证码的url
router.register(r'codes', SmsCodeViewset, base_name='codes')
# 配置users注册的url
router.register(r'users', UserViewset, base_name='users')
# 配置约运动的接口
router.register(r'schedules', ScheduleViewset, base_name='schedules')
# 配置加入的约运动的url接口
router.register(r'my', JoinScheduleViewset, base_name='my')
# 配置喜爱的运动接口
router.register(r'favsports', FavViewset, base_name='favsports')
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # 配置文件及图片上传路径
    # 配置drf文档
    url('^docs/', include_docs_urls(title='悦运动')),
    url('^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # drf登录配置
    url(r'^api-auth/', include('rest_framework.urls')),
    url('^', include(router.urls)),
    # jwt的认证接口
    url(r'^login/$', obtain_jwt_token),
]
