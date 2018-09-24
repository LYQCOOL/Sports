# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/29 18:20'
from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator
from rest_framework.permissions import IsAuthenticated

from .models import *
from schools.serializers import SchoolSerializer1
from users.serializers import UserDetailSerializer, UserUpdateSerializer
from .current import CurrentSchoolDefault


class SportsSerializer(serializers.ModelSerializer):
    '''
    运动序列化
    '''

    class Meta:
        model = Sports
        fields = '__all__'


class ScheduleSerializer(serializers.Serializer):
    '''
    约运动序列化
    '''
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    school = serializers.HiddenField(
        default=CurrentSchoolDefault()
    )
    sport = serializers.PrimaryKeyRelatedField(queryset=Sports.objects.all(), required=True, label='运动')
    sport_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', label='运动开始时间')
    sport_end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', label='运动结束时间')
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    address = serializers.CharField(required=True, max_length=25, error_messages={'max_length': '详细地址长度不能超过25'},
                                    label='详细地址')
    # school = serializers.HiddenField(default=Schools.objects.filter(category_type=1).first())
    now_people = serializers.IntegerField(read_only=True, default=1)
    people_nums = serializers.IntegerField(min_value=2, required=True, max_value=20,
                                           error_messages={'required': '请填写总人数', 'min_value': '人数至少为两人，一起运动更愉快!',
                                                           'max_value': '请按照运动适当指定人数，不能超过20人', },
                                           label='约定总人数'
                                           )

    def validate(self, attrs):
        now_time = datetime.now()
        sport_time = attrs['sport_time']
        sport_end_time = attrs['sport_end_time']
        if sport_time <= now_time:
            raise serializers.ValidationError('约定运动开始的时间应该大于目前时间')
        if (sport_time - now_time).days >= 10:
            raise serializers.ValidationError('只能发布十天以内的约运动')
        if (sport_end_time - sport_time).seconds <= 1800:
            raise serializers.ValidationError('约定运动结束时间应该大于开始时间，且应该在半小时以上')
        if (sport_end_time - sport_time).days != 0:
            raise serializers.ValidationError('运动得适量哦，结束时间应小于一天')
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        sport_time = validated_data['sport_time']
        validated_data['now_people'] = 1
        # validated_data['school'] = self.context['request'].user.school
        validated_data['join_type'] = 1
        validated_data['status'] = 2
        existed = Schedule.objects.filter(user=user, sport_time=sport_time)
        if existed:
            pass
        else:
            existed = Schedule.objects.create(**validated_data)
        return existed

    class Meta:
        model = Schedule
        validators = [
            UniqueTogetherValidator(
                queryset=Schedule.objects.all(),
                fields=('user', 'sport_time'),
                message='该时间段已有预约'
            )
        ]
        fields = (
            'user', 'sport', 'address', 'sport_time', 'sport_end_time', 'people_nums', 'add_time', 'now_people',
            'school')


class ScheduleDetailSerializer(serializers.ModelSerializer):
    '''
    约运动详情
    '''
    school = SchoolSerializer1()
    user = UserDetailSerializer()
    sport = SportsSerializer()
    sport_time = serializers.DateTimeField(required=True, format='%Y-%m-%d %H:%M:%S')
    sport_end_time = serializers.DateTimeField(required=True, format='%Y-%m-%d %H:%M:%S')
    joiners = serializers.SerializerMethodField()

    def get_joiners(self, obj):
        all_joiners = JoinSchedule.objects.filter(schedule_id=obj.id, )
        all_joiners_json = JoinScheduleDetailSerializer(all_joiners, many=True,
                                                        context={'request': self.context['request']}).data
        return all_joiners_json

    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleListSerializer(serializers.ModelSerializer):
    '''
    约运动序列化
    '''
    user = UserUpdateSerializer()
    sport = SportsSerializer()
    sport_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', label='运动时间')
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Schedule
        fields = ('user', 'sport', 'address', 'sport_time', 'now_people', 'people_nums', 'add_time')


class MyJoinScheduleDetailSerializer(serializers.ModelSerializer):
    '''
    我加入的约运动详情序列化
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    schedule = ScheduleDetailSerializer()
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = JoinSchedule
        fields = '__all__'


class JoinScheduleDetailSerializer(serializers.ModelSerializer):
    '''
    加入约运动详情人员序列化
    '''
    user = UserDetailSerializer()
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = JoinSchedule
        fields = '__all__'


class MyJoinScheduleSerializer(serializers.ModelSerializer):
    '''
    加入约运动序列化
    '''
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    def create(self, validated_data):
        user = self.context['request'].user
        schedule = validated_data['schedule']
        if Schedule.objects.filter(user=schedule.user, id=schedule.id).first().user == user:
            raise serializers.ValidationError('您是该运动的发起人，已默认加入')
        if schedule.sport_time <= datetime.now():
            raise serializers.ValidationError('运动已经开始，请与发起人直接联系是否成功进行并加入')
        double_status = False
        schedules = JoinSchedule.objects.filter(user=user, schedule__sport_time__gt=datetime.now())
        if schedules:
            for s in schedules:
                if s.schedule.sport_time > schedule.sport_end_time or schedule.sport_time >= s.schedule.sport_end_time:
                    pass
                else:
                    double_status = True
                    break
        if double_status:
            raise serializers.ValidationError({"time_error": "与你已有的预约运动时间冲突"})
        else:
            existed = JoinSchedule.objects.create(**validated_data)
        return existed

    class Meta:
        model = JoinSchedule
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=JoinSchedule.objects.all(),
                fields=('user', 'schedule'),
                message='已经加入'
            )
        ]


class FavSportsSerializer(serializers.ModelSerializer):
    '''
    我喜爱的运动序列化
    '''
    student = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    sport = serializers.PrimaryKeyRelatedField(queryset=Sports.objects.all(), required=True,label='运动')
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Sport_Fav
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Sport_Fav.objects.all(),
                fields=('student', 'sport'),
                message='已经添加致喜爱的运动'
            )
        ]
