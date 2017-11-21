from django.contrib import admin

# Register your models here.

from django.contrib import admin


# Register your models here.
from domeplaylist import models
from domeplaylist.models import PlayList


class PlayItemInline(admin.TabularInline):
    model = models.PlayItem
    extra = 1


class PlayListAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'zodiac_choice',
    )

    inlines = (PlayItemInline,)


admin.site.register(PlayList, PlayListAdmin)
