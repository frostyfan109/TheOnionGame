from django.contrib import admin
from .models import *
from common.util import toPercentString

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','percentCorrect','real')
    fields = [field.name for field in Article._meta.fields if field.name != 'id']

    def percentCorrect(self,obj):
        return toPercentString(obj.getPercentIncorrect())

admin.site.register(Article,ArticleAdmin)
