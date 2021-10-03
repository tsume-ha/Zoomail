import datetime

from django.contrib import admin
from custom_admin.admin import custom_admin_site
from .models import Live, Song


class SongInlineAdmin(admin.TabularInline):
    model = Song
    extra = 0
    fields = ('track_num', 'song_name', 'file', 'length')
    readonly_fields = ('length', )


class LiveAdmin(admin.ModelAdmin):
    inlines = [SongInlineAdmin, ]
    fields = ('live_name', 'recorded_at', 'created_at', 'updated_at', 'updated_by')
    readonly_fields = ('created_at', 'updated_at', 'updated_by')
    list_display = ('id', 'live_name', 'recorded_at')
    list_display_links = ('id', 'live_name')

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
            obj.updated_at = datetime.datetime.now()
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for instance in instances:
                instance.updated_by = request.user
                instance.updated_at = datetime.datetime.now()
                instance.save()
            formset.save_m2m()


class SongAdmin(admin.ModelAdmin):
    model = Song
    fields = ('track_num', 'song_name', 'file', 'length', 'created_at', 'updated_at', 'updated_by')
    readonly_fields = ('length', 'created_at', 'updated_at', 'updated_by')
    list_display = ('id', 'song_name', 'live', 'track_num')
    list_display_links = ('id', 'track_num', 'song_name')
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
            obj.updated_at = datetime.datetime.now()
        super().save_model(request, obj, form, change)



admin.site.register(Live, LiveAdmin)
admin.site.register(Song, SongAdmin)

custom_admin_site.register(Live, LiveAdmin)
custom_admin_site.register(Song, SongAdmin)

