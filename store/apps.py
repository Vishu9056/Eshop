from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ProfilesConfig(AppConfig):
    name = 'Eshop.store'
    verbose_name = _('store')

    def ready(self):
        import Eshop.store.signals  

class StoreConfig(AppConfig):
    name = 'store'
