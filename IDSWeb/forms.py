from django import forms
from .models import Rule

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['name', 'pattern', 'severity'] 
        
class PatternForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['pattern'] 