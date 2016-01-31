from django.contrib import admin
from news.models import New, Attach, Reply, Comment


class AttachInline(admin.StackedInline):
    model = Attach
    extra = 1


class NewAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'status', 'marked']
    inlines = [AttachInline]
    list_display = ('title', 'text', 'status', 'marked', 'pub_date')


class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 1


class CommentAdmin(admin.ModelAdmin):
    fields = ['new', 'author', 'text']
    inlines = [ReplyInline]
    list_display = ('new', 'author', 'text', 'pub_date')
    
    list_filter = ['pub_date']

admin.site.register(New, NewAdmin)
admin.site.register(Comment, CommentAdmin)