from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Faq, Rule


class RuleModelForm(forms.ModelForm):
    """Model Form to override default Rule modelAdmin Form"""
    rule = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Rule
        fields = '__all__'


class FaqModelForm(forms.ModelForm):
    """Model Form to override default Faq modelAdmin Form"""
    question = forms.CharField(widget=CKEditorWidget())
    answer = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Faq
        fields = '__all__'
