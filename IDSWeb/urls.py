from django.urls import path
from IDSWeb.views import AlertListView
app_name = 'IDSWeb'
urlpatterns = [
    path('', AlertListView.as_view(), name='alert_list'),
]