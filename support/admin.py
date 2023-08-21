"""
How we used html safe in django:
https://gist.github.com/lambdamusic/4734421
"""
from django.contrib import admin
from django.utils.html import strip_tags
from .models import Faq, UserMessage, Rule
from .forms import FaqModelForm, RuleModelForm


@admin.register(Faq)
class FaqModelAdmin(admin.ModelAdmin):
    form = FaqModelForm
    list_display = ['question_text', 'answer_text']
    list_display_links = ['question_text', 'answer_text']
    
    @admin.display(description="question")
    def question_text(self, obj):
        return strip_tags(obj.question)
    
    @admin.display(description="answer")
    def answer_text(self, obj):
        return strip_tags(obj.answer)
    


@admin.register(Rule)
class RuleModelAdmin(admin.ModelAdmin):
    form = RuleModelForm


@admin.register(UserMessage)
class FaqModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'created']