from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Account)
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(Token)

