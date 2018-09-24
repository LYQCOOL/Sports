from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'excersise'
    verbose_name='运动'
    def ready(self):
        import excersise.signals
