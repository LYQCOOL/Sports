from rest_framework import viewsets
from rest_framework import mixins

from .serializers import *


class SchoolViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = SchoolSerializer3
    queryset = Schools.objects.filter(category_type=1)
