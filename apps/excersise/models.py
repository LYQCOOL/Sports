from datetime import datetime
from django.db import models

from users.models import *
from schools.models import Schools


# Create your models here.
class Sports(models.Model):
    '''
    运动表
    '''
    school = models.ForeignKey(Schools, verbose_name='学校', on_delete=models.CASCADE)
    sport_name = models.CharField(max_length=30, verbose_name='运动项目')
    image = models.ImageField(upload_to='sports/%Y/%m', verbose_name='运动封面图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '运动项目'
        verbose_name_plural = verbose_name
        unique_together = ('school', 'sport_name')

    def __str__(self):
        return self.sport_name


class Sport_Fav(models.Model):
    '''
    学生喜爱运动项目表
    '''
    student = models.ForeignKey(UserProfile, verbose_name='学生', on_delete=models.CASCADE, default=1)
    sport = models.ForeignKey(Sports, verbose_name='运动项目', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '学生喜爱的运动'
        verbose_name_plural = verbose_name
        unique_together = ('student', 'sport')

    def __str__(self):
        return self.student.username + '--' + self.sport.sport_name


class Schedule(models.Model):
    '''
    发起约运动
    '''
    Status = ((1, '已完成'), (2, '待人加入'), (3, '已取消'))
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='发起人')
    join_type = models.BooleanField(verbose_name='是否发起人')
    now_people = models.IntegerField(verbose_name='已有人数', null=True, blank=True)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, verbose_name='学校', default='')
    sport = models.ForeignKey(Sports, on_delete=models.CASCADE, verbose_name='运动项目')
    address = models.CharField(verbose_name='约定地点', max_length=100)
    sport_time = models.DateTimeField(verbose_name='约定运动开始时间')
    sport_end_time = models.DateTimeField(verbose_name='约定运动结束时间', default='')
    people_nums = models.IntegerField(verbose_name='人数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    status = models.IntegerField(choices=Status, verbose_name='状态')

    class Meta:
        verbose_name = '发起约运动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sport.sport_name + '-' + str(self.sport_time)


class JoinSchedule(models.Model):
    '''
    加入的运动
    '''
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name='加入的运动')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '加入运动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.schedule_id) + '--' + str(self.user_id)
