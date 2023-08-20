from django.db import models
from django.utils.translation import gettext_lazy as _



class Rule(models.Model):
    """It has a container that contains a text field with all the rules in one field"""
    rule = models.TextField(verbose_name=_('rules'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Rule'
        verbose_name_plural = 'Rule'
        ordering = ['-updated']

    def __str__(self) -> str:
        return f'rule({self.id})'

class Faq(models.Model):
    """Every frequently asked question have a question and answer in it"""
    question = models.TextField(verbose_name=_('question'))
    answer = models.TextField(verbose_name=_('answer'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Faq'
        verbose_name_plural = 'Faq'
        ordering = ['-updated']
    
    def __str__(self) -> str:
        return f'question({self.id})'



class UserMessage(models.Model):
    """In faq page, users can send message via form"""
    email = models.EmailField(verbose_name=_('emal'))
    message = models.TextField(verbose_name=_('message'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'UserMessage'
        verbose_name_plural = 'UserMessage'
        ordering = ['-updated']
    
    def __str__(self) -> str:
        return f'user_message({self.id})'
