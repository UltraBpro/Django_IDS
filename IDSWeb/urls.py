from django.urls import path
from IDSWeb.views import AlertListView, add_rule_view, edit_pattern
app_name = 'IDSWeb'
urlpatterns = [
    path('', AlertListView.as_view(), name='alert_list'),
    path('add-rule/', add_rule_view, name='add_rule'),
    path('edit-pattern/<int:alert_id>/', edit_pattern, name='edit_pattern'),
]
