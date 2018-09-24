from rest_framework.compat import (
    InvalidTimeError, MaxLengthValidator, MaxValueValidator,
    MinLengthValidator, MinValueValidator, unicode_repr, unicode_to_repr
)
class CurrentSchoolDefault(object):
    def set_context(self, serializer_field):
        self.school = serializer_field.context['request'].user.school

    def __call__(self):
        return self.school

    def __repr__(self):
        return unicode_to_repr('%s()' % self.__class__.__name__)


