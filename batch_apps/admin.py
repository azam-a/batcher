from django.contrib import admin
from batch_apps.models import App, Pattern, Day, Execution
from django.db import models
from django.forms import TextInput
from batch_apps.integration import execute_end_to_end_tasks

admin.site.index_template = 'admin/my_index.html'


class PatternInline(admin.TabularInline):
    model = Pattern
    extra = 0


class AppAdmin(admin.ModelAdmin):
    actions = ['activate_apps', 'deactivate_apps']
    list_display = ('name', 'is_active', 'frequency', 'country', 'category', )
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['is_active']}),
        (None, {'fields': ['frequency']}),
        (None, {'fields': ['country']}),
        (None, {'fields': ['category']}),
        (None, {'fields': ['repo']}),
        ('Description', {'fields': ['description'], }),
    ]
    inlines = [PatternInline]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '150'})},
    }

    def activate_apps(self, request, queryset):
        queryset.update(is_active=True)
    activate_apps.short_description = "Activate selected Apps"

    def deactivate_apps(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_apps.short_description = "Deactivate selected Apps"


class ExecutionInline(admin.TabularInline):
    model = Execution
    readonly_fields = ('day', 'app')
    extra = 0


class DayAdmin(admin.ModelAdmin):
    actions = ['execute_end_to_end_tasks_on_day']
    model = Day
    inlines = [ExecutionInline]

    def execute_end_to_end_tasks_on_day(self, request, queryset):
        for day in queryset:
            execute_end_to_end_tasks(day.date)
    execute_end_to_end_tasks_on_day.short_description = "Generate objects and process emails"


admin.site.register(App, AppAdmin)
admin.site.register(Day, DayAdmin)
