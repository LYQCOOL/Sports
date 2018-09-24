import xadmin
from .models import *


class SchoolAdmin(object):
    # 可以是列表[],也可以是元组()，但使用元组只有一个字段是一定要加逗号
    list_display = ['name', 'category_type', 'parent_category']
    # 配置在哪些字段搜索
    search_fields = ['name', 'province', 'city', 'district', 'address']
    # 配置过滤字段
    list_filter = ['name', 'province', 'city', 'district', 'address', 'add_time']
    ordering = ['category_type','parent_category']


xadmin.site.register(Schools, SchoolAdmin)
