'''注册'''
from django.apps import AppConfig


class Oomph6Config(AppConfig):
    name = 'oomph6'
    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('oomph6')
