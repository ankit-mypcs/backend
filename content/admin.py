from django.contrib import admin
from .models import Subject, Chapter, Question, KeyTerm


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'subject', 'number', 'is_active']
    list_filter = ['subject', 'is_active']
    search_fields = ['title', 'code']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'get_stem_preview', 'chapter', 'difficulty', 'correct_answer', 'exam_source', 'year', 'is_active']
    list_filter = ['difficulty', 'exam_source', 'year', 'chapter__subject', 'is_active', 'question_type']
    search_fields = ['question_id', 'stem']
    readonly_fields = ['created_at', 'updated_at']

    def get_stem_preview(self, obj):
        return obj.stem[:75] + '...' if len(obj.stem) > 75 else obj.stem
    get_stem_preview.short_description = 'Question'


@admin.register(KeyTerm)
class KeyTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'subject']
    list_filter = ['subject']
    search_fields = ['term', 'definition']
    filter_horizontal = ['related_questions']
