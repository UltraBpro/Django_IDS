from django.contrib import admin
from .models import Rule, Alert

# Register your models here.

class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity', 'pattern')  
    search_fields = ('name', 'pattern')  
    list_filter = ('severity',)  

class AlertAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'attack_type', 'severity', 'log_entry')  
    search_fields = ('attack_type', 'log_entry')  
    list_filter = ('severity', 'timestamp')  

admin.site.register(Rule, RuleAdmin)
admin.site.register(Alert, AlertAdmin)
