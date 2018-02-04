from django.contrib import admin

# Register your models here.

from django.contrib import admin


# Register your models here.
from domeplaylist.models import PlayList, Track


class TrackInline(admin.TabularInline):
    model = Track
    extra = 1


class PlayListAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'title',
        'theme',
    )

    inlines = (TrackInline,)


class TrackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'playlist',
        'title',
        'text',
        'image',
    )




admin.site.register(PlayList, PlayListAdmin)
admin.site.register(Track, TrackAdmin)
