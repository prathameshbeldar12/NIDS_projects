from django.apps import AppConfig


class NidsDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nids_dashboard'

    def ready(self):
        import nids_dashboard.signals