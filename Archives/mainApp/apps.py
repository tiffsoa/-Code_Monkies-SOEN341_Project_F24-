from django.apps import AppConfig

#we do not have to worry about this file

class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainApp'
