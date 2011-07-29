from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from blocks.models import Block

class AdminBlock(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'block_key', 'status')

admin.site.register(Block, AdminBlock)
