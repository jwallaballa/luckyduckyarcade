# arcade_app/apps.py

from django.apps import AppConfig

"""
App configuration for the arcade_app Django application.
"""
class ArcadeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'arcade_app'
