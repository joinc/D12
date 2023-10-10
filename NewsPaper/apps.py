from django.apps import AppConfig


class NewspaperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NewsPaper'

    def ready(self):
        import NewsPaper.signals
