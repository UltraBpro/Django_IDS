from django.urls import path
from IDSWeb.views import AlertListView, RuleListView, RuleDeleteView, export_rules, import_rules, start_ids, stop_ids, get_ids_status
app_name = 'IDSWeb'
urlpatterns = [
    path('', AlertListView.as_view(), name='alert_list'),
    path('rules/', RuleListView.as_view(), name='rule_list'),
    path('rules/<int:pk>/delete/', RuleDeleteView.as_view(), name='rule_delete'),
    path('rules/export/', export_rules, name='export_rules'),
    path('rules/import/', import_rules, name='import_rules'),
    path('start-ids/', start_ids, name='start_ids'),
    path('stop-ids/', stop_ids, name='stop_ids'),
    path('ids-status/', get_ids_status, name='ids_status'),
]