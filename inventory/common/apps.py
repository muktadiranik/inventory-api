from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory.common'
    verbose_name = "Settings"

    def ready(self):
        import inventory.common.signals
