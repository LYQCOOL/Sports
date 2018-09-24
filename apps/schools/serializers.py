# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/30 10:16'
from rest_framework import serializers

from .models import *


class SchoolSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Schools
        fields = ('name', 'category_type', 'sub_cat', 'add_time')


class SchoolSerializer2(serializers.ModelSerializer):
    sub_cat = SchoolSerializer1(many=True)

    class Meta:
        model = Schools
        fields = ('name', 'category_type', 'sub_cat', 'add_time')


class SchoolSerializer3(serializers.ModelSerializer):
    sub_cat = SchoolSerializer2(many=True)

    class Meta:
        model = Schools
        fields = '__all__'
