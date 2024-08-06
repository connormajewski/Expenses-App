from django.apps import AppConfig


class SpendingsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spendingsite'

    def ready(self):

        print("STARTING...")
