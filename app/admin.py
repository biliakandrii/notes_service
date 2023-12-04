from django.contrib import admin

from .models import User, Note


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username',)


class NoteAdmin(admin.ModelAdmin):
    list_display = ('header',)
    search_fields = ('header',)


admin.site.register(User, UserAdmin)
admin.site.register(Note, NoteAdmin)
