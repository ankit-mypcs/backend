from django.contrib import admin
from .models import Subject, Unit


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1
    fields = ('name', 'slug', 'icon', 'sort_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'unit_count', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [UnitInline]

    @admin.display(description='Units')
    def unit_count(self, obj):
        return obj.units.count()


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('subject', 'is_active')
    search_fields = ('name', 'subject__name')
    prepopulated_fields = {'slug': ('name',)}
