import django_filters
from django.db.models import Q

from .models import Schedule


class SportsFilter(django_filters.rest_framework.FilterSet):
    sport_name = django_filters.CharFilter(method='to_sport_name',label='运动项目')
    max_sport_time = django_filters.DateTimeFilter(field_name='sport_time', lookup_expr='lte', label='运动时间小于',
                                                   help_text='运动时间小于于某个时间')
    min_sport_time = django_filters.DateTimeFilter(field_name='sport_time', lookup_expr='gte', label='运动时间大于',
                                                   help_text='运动时间大于某个时间')

    def to_sport_name(self,queryset,name,value):
        return queryset.filter(sport__sport_name__icontains=value)

    class Meta:
        model = Schedule
        fields = ['min_sport_time', 'max_sport_time', 'sport_name']
