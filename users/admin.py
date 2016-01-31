from django.contrib import admin
from users.models import Profile, Portfolio, Skills, Attach

class AttachInline(admin.StackedInline):
    model = Attach
    extra = 1

class PortfolioAdmin(admin.ModelAdmin):
    fields = ['user', 'title', 'description', 'link']
    inlines = [AttachInline]
    list_display = ('user', 'title', 'description', 'link', 'created')

admin.site.register(Profile)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Skills)
admin.site.register(Attach)