from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

class MeasurementsConfig(AppConfig):
	name = "measurements"
	verbose_name = 'Measurement between 2 locations'