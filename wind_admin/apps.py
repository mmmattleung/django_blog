from django.apps import AppConfig


class WindAdminConfig(AppConfig):
    name = 'wind_admin'

    def ready(self, *args, **kwargs):
        super(WindAdminConfig, self).ready()

        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules('wind')