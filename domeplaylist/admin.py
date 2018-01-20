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
        'title',
        'theme',
    )

    inlines = (TrackInline,)


admin.site.register(PlayList, PlayListAdmin)
