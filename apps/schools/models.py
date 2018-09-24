from django.db import models
from datetime import datetime


# Create your models here.
class Schools(models.Model):
    '''
    学校表
    '''
    CATEGORY_TYPE = ((1, '学校'), (2, '学院'), (3, '专业'))
    name = models.CharField(max_length=50, verbose_name='名字')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat", on_delete=models.CASCADE)
    province = models.CharField(max_length=100, default="", verbose_name="省份", null=True, blank=True)
    city = models.CharField(max_length=100, default="", verbose_name="城市", null=True, blank=True)
    district = models.CharField(max_length=100, default="", verbose_name="区域", null=True, blank=True)
    address = models.CharField(max_length=100, default="", verbose_name="详细地址", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
