"""
content/admin.py — Django Admin for all 27 content models
"""
from django.contrib import admin
from content.models import (
    State, SourceBook, Subject, Part, Unit, Chapter, Topic, SubTopic,
    MicroTopic, Fact, Site, TimelineEvent, GlossaryTerm, ExamIntelEntry,
    ComparisonMatrix, Visual, Exercise, Exam, ExamSession, Paper,
    PaperSection, Competency, PrelimsPYQ, MainsPYQ, QuestionAppearance,
    ExamSource, FactQuestionLink, SiteQuestionLink,
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'sort_order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'code', 'sort_order']
    list_filter = ['subject']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'part', 'code', 'sort_order']
    list_filter = ['part__subject', 'part']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'chapter_number', 'question_count', 'is_active']
    list_filter = ['unit__part__subject', 'unit__part', 'unit']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'chapter', 'sort_order']
    list_filter = ['chapter__unit__part']
    search_fields = ['name']


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ['short_text', 'chapter', 'source_sheet', 'topic']
    list_filter = ['source_sheet', 'chapter']
    search_fields = ['text']

    def short_text(self, obj):
        return obj.text[:80]


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'state_region', 'period', 'chapter']
    list_filter = ['chapter']
    search_fields = ['name', 'key_findings']


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ['date_text', 'event_short', 'chapter']
    list_filter = ['chapter']

    def event_short(self, obj):
        return obj.event[:80]


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'chapter']
    list_filter = ['chapter']
    search_fields = ['term', 'definition']


@admin.register(ExamIntelEntry)
class ExamIntelEntryAdmin(admin.ModelAdmin):
    list_display = ['category', 'chapter', 'detail_short']
    list_filter = ['category', 'chapter']

    def detail_short(self, obj):
        return obj.detail[:80]


@admin.register(Visual)
class VisualAdmin(admin.ModelAdmin):
    list_display = ['ref_code', 'description', 'chapter']
    list_filter = ['chapter']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['exercise_type', 'question_short', 'chapter']
    list_filter = ['exercise_type', 'chapter']

    def question_short(self, obj):
        return obj.question[:80]


@admin.register(PrelimsPYQ)
class PrelimsPYQAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'stem_short', 'year', 'exam_source',
                    'difficulty', 'review_status']
    list_filter = ['exam_source', 'year', 'difficulty', 'review_status']
    search_fields = ['question_id', 'stem']

    def stem_short(self, obj):
        return obj.stem[:80]


# Register remaining models simply
for model in [State, SourceBook, SubTopic, MicroTopic, ComparisonMatrix,
              Exam, ExamSession, Paper, PaperSection, Competency,
              MainsPYQ, QuestionAppearance, ExamSource,
              FactQuestionLink, SiteQuestionLink]:
    admin.site.register(model)
