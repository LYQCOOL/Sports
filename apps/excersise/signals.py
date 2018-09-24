# _*_ encoding:utf-8 _*_
__author__ = 'LYQ'
__data__ = '2018/8/21 20:15'
from django.conf import settings
from .models import Schedule, JoinSchedule
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import JoinSchedule


# 通过信号实现人数加一
@receiver(post_save, sender=JoinSchedule)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        schedule = instance.schedule
        if schedule.now_people < schedule.people_nums:
            schedule.now_people += 1
            schedule.save()
        else:
            pass


# 通过信号实现人数减一
@receiver(post_delete, sender=JoinSchedule)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    schedule = instance.schedule
    schedule.now_people -= 1
    schedule.save()



