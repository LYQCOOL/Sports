# _*_ encoding:utf-8 _*_
import re
from datetime import datetime
from datetime import timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from Sports.settings import REGEX_MOBILE
from .models import VerifyCode
from schools.models import Schools
from schools.serializers import SchoolSerializer3, SchoolSerializer1

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    '''
    注册手机号和验证码序列化
    '''
    mobile = serializers.CharField(max_length=11, min_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        '''
        # 验证手机是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号非法')
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')
        on_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=on_minute_ago, mobile=mobile):
            raise serializers.ValidationError('距离上一次发送未超过60秒')
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册序列化
    '''
    # write_only=True,不会拿该字段来序列化,labe标签名，help_text：docs文档中description
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label='验证码',
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "验证码不能为空",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 }, help_text='验证码')
    mobile = serializers.CharField(required=True, allow_blank=False,
                                   validators=[UniqueValidator(queryset=User.objects.all(), message='该手机已经注册')],
                                   max_length=11, min_length=11,
                                   error_messages={'max_length': '手机格式错误',
                                                   'min_length': '手机格式错误'},
                                   label='手机号')
    name = serializers.CharField(required=True, allow_blank=False, max_length=4, min_length=2,
                                 error_messages={'max_length': '姓名格式错误，长度应该小于等于4', 'min_length': '姓名格式错误，长度应该大于等于2'},
                                 label='姓名')
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, label='密码', max_length=12,
                                     min_length=6, required=True,
                                     error_messages={'max_length': '密码长度应该在6到12个字符之间',
                                                     'min_length': '密码长度应该在6到12个字符之间'})
    password_confirm = serializers.CharField(style={"input_type": "password"}, write_only=True, label='再次输入密码',
                                             required=True)

    def validate_code(self, code):
        verify_codes = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_codes:
            last_verfycode = verify_codes[0]
            five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minute_ago > last_verfycode.add_time:
                raise serializers.ValidationError('验证码过期')
            if code != last_verfycode.code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    # 作用于所有字段
    def validate_mobile(self, mobile):
        '''
        验证手机号码
        '''
        # 验证手机是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号非法')
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')
        return mobile

    def validate(self, attrs):
        mobile = attrs['mobile']
        mobile_confirm = attrs['mobile_confirm']
        if mobile != mobile_confirm:
            raise serializers.ValidationError('两次密码不一致')
        attrs["username"] = mobile
        del attrs["code"]
        del attrs['mobile_confirm']
        return attrs

    class Meta:
        model = User
        fields = ('school', 'institude', 'profession', 'mobile', 'code', 'name', 'password', 'password_confirm', 'id')


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户详情页序列化类
    '''
    school = SchoolSerializer3()

    class Meta:
        model = User
        fields = ('name', 'birthday', 'gender', 'email', 'mobile', 'school')


class UserUpdateSerializer(serializers.ModelSerializer):
    '''
    用户详情页序列化类
    '''

    class Meta:
        model = User
        fields = ('name', 'birthday', 'gender', 'email', 'mobile')
