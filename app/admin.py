from django.contrib import admin

from .models import User, Note


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'number_of_notes')
    search_fields = ('username',)
    list_filter = ('numberOfNotes',)
    sortable_by = ('numberOfNotes',)

    def number_of_notes(self, obj):
        return obj.numberOfNotes

class NoteAdmin(admin.ModelAdmin):
    list_display = ('header', 'authors_')
    search_fields = ('header',)


admin.site.register(User, UserAdmin)
admin.site.register(Note, NoteAdmin)
