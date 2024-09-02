from django.apps import AppConfig
import os

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        upload_dir = os.path.join('media', 'uploads')
        repo_dir = os.path.join('media', 'repos')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)
