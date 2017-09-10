from django.contrib import admin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    prepopulated_fields = {'slug': ('name',)}

class EuroAuchanNamesAdmin(admin.ModelAdmin):

    fields = ['euro_name', 'auchan_name', 'pol_num']

admin.site.register(Category, CategoryAdmin)
admin.site.register(EuroAuchanNames, EuroAuchanNamesAdmin)
