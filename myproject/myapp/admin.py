from django.contrib import admin
from .models import Post, Event, EventVisitor, PostForm, EventForm


class PostAdmin(admin.ModelAdmin):
    form = PostForm


admin.site.register(Post, PostAdmin)


class EventAdmin(admin.ModelAdmin):
    form = EventForm


admin.site.register(Event, EventAdmin)


class EventVisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event')
    list_filter = ('event',)
    search_fields = ('name', 'email')


admin.site.register(EventVisitor, EventVisitorAdmin)
