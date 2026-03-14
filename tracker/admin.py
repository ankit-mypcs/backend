from django.contrib import admin
from .models import BuildTask, BuildSubTask


class BuildSubTaskInline(admin.TabularInline):
    model = BuildSubTask
    extra = 1
    fields = ['subtask_id', 'title', 'status', 'depends_on', 'completed_at']


@admin.register(BuildTask)
class BuildTaskAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'title', 'session', 'group', 'status',
                    'subtask_summary', 'completed_at']
    list_filter = ['status', 'session', 'group', 'module']
    list_editable = ['status']
    search_fields = ['task_id', 'title', 'description']
    list_per_page = 50
    inlines = [BuildSubTaskInline]
    fieldsets = (
        (None, {
            'fields': ['task_id', 'title', 'session', 'group', 'module',
                        'status', 'priority'],
        }),
        ('Details', {
            'fields': ['description', 'depends_on', 'models_created',
                        'files_changed'],
            'classes': ['collapse'],
        }),
        ('Notes & Dates', {
            'fields': ['notes', 'started_at', 'completed_at'],
            'classes': ['collapse'],
        }),
    )

    @admin.display(description='Subtasks')
    def subtask_summary(self, obj):
        total = obj.subtasks.count()
        if total == 0:
            return '-'
        done = obj.subtasks.filter(status='done').count()
        return f"{done}/{total} done"


@admin.register(BuildSubTask)
class BuildSubTaskAdmin(admin.ModelAdmin):
    list_display = ['subtask_id', 'title', 'task', 'status', 'completed_at']
    list_filter = ['status', 'task']
    list_editable = ['status']
