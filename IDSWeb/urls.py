from django.urls import path
from IDSWeb.views import AlertListView, RuleListView, RuleDeleteView, export_rules, import_rules
app_name = 'IDSWeb'
urlpatterns = [
    path('', AlertListView.as_view(), name='alert_list'),
    path('rules/', RuleListView.as_view(), name='rule_list'),
    path('rules/<int:pk>/delete/', RuleDeleteView.as_view(), name='rule_delete'),
    path('rules/export/', export_rules, name='export_rules'),
    path('rules/import/', import_rules, name='import_rules'),
]