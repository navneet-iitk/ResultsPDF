from django.urls import path
from .views import SuggestedLinksViewset


urlpatterns = [
    path('data-sync', SuggestedLinksViewset.as_view({'post':'data_sync'}), name='data-sync'),
]