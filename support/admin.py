from django.contrib import admin
from .models import Faq, UserMessage, Rule


admin.site.register([Faq, UserMessage, Rule])
