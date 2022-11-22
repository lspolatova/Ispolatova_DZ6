from django.contrib import admin

# Register your models here.
from chats.models import Chat, Category, Files, Messages
admin.site.register(Chat)
admin.site.register(Category)
admin.site.register(Files)
admin.site.register(Messages)
