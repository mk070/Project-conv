from django.apps import AppConfig
import os

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        UPLOADS_DIR = 'UPLOADS'
        if not os.path.exists(UPLOADS_DIR):
            os.makedirs(UPLOADS_DIR)