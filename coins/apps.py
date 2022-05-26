from django.apps import AppConfig


class CoinsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coins'

    def ready(self):
        print("at ready")
        import coins.signals
