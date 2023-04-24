from django.contrib import admin
from .models import Post, Event, EventVisitor

admin.site.register(Post)
admin.site.register(Event)


class EventVisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event')
    list_filter = ('event',)
    search_fields = ('name', 'email')


admin.site.register(EventVisitor, EventVisitorAdmin)