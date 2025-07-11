from django.apps import AppConfig

class AtIdentityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'at_identity'
    verbose_name = 'AT Identity'
    
    def ready(self):
        import at_identity.signals