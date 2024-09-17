from django.urls import path
from IDSWeb.views import AlertListView

urlpatterns = [
    path('alerts/', AlertListView.as_view(), name='alert_list'),
]