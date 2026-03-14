from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Subject, Unit, Chapter, Topic, SubTopic, MicroTopic,
    Exam, ExamSession, Paper, Part, Competency, MainsPYQ, PrelimsPYQ,
    QuestionAppearance, ExamSource,
)
from .resources import PrelimsPYQResource


# ── Inlines ──────────────────────────────────────────────

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1
    fields = ('name', 'slug', 'icon', 'sort_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


class ExamSessionInline(admin.TabularInline):
    model = ExamSession
    extra = 0
    fields = ('year', 'prelims_date', 'mains_date', 'is_active')


# ── Subject & Unit ───────────────────────────────────────

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'icon', 'name', 'unit_count', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [UnitInline]

    @admin.display(description='Units')
    def unit_count(self, obj):
        return obj.units.count()


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'chapter_count', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('subject', 'is_active')
    search_fields = ('name', 'subject__name')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Chapters')
    def chapter_count(self, obj):
        return obj.chapters.count()


# ── Chapter ─────────────────────────────────────────────

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    fields = ('name', 'code', 'slug', 'sort_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'unit', 'topic_count', 'question_count', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('unit__subject', 'is_active')
    search_fields = ('name', 'code', 'unit__name')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('unit',)

    @admin.display(description='Topics')
    def topic_count(self, obj):
        return obj.topics.count()


# ── Topic & SubTopic ───────────────────────────────────

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1
    fields = ('name', 'code', 'slug', 'sort_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


class SubTopicInline(admin.TabularInline):
    model = SubTopic
    extra = 1
    fields = ('name', 'sort_order', 'is_active')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'chapter', 'subtopic_count', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('chapter__unit__subject', 'is_active')
    search_fields = ('name', 'code', 'chapter__name')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('chapter',)
    inlines = [SubTopicInline]

    @admin.display(description='SubTopics')
    def subtopic_count(self, obj):
        return obj.subtopics.count()


@admin.register(SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('topic__chapter__unit__subject', 'is_active')
    search_fields = ('name', 'topic__name')
    raw_id_fields = ('topic',)


# ── MicroTopic ────────────────────────────────────────────

@admin.register(MicroTopic)
class MicroTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_topic', 'sort_order', 'is_active')
    list_filter = ('sub_topic__topic__chapter', 'sub_topic', 'is_active')
    search_fields = ('name', 'name_hi')
    list_editable = ('sort_order',)


# ── Exam & ExamSession ──────────────────────────────────

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'short_name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ExamSessionInline]


@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'year', 'prelims_date', 'mains_date',
                    'posts_advertised', 'students_final_selected', 'is_active')
    list_filter = ('exam', 'year', 'is_active')
    search_fields = ('exam__name',)


# ── Paper ────────────────────────────────────────────────

class PartInline(admin.TabularInline):
    model = Part
    extra = 1
    fields = ('name', 'short_name', 'slug', 'marks', 'sort_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'exam_stage', 'paper_type',
                    'total_marks', 'duration_minutes', 'is_qualifying',
                    'negative_marking', 'part_count', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('exam_stage', 'paper_type', 'is_qualifying',
                   'negative_marking', 'is_active')
    search_fields = ('name', 'short_name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PartInline]

    @admin.display(description='Parts')
    def part_count(self, obj):
        return obj.parts.count()


# ── Part ────────────────────────────────────────────────

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'paper', 'marks', 'question_count', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('paper', 'is_active')
    search_fields = ('name', 'short_name', 'paper__short_name')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('paper',)


# ── Competency ───────────────────────────────────────────

@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'blooms_level', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('blooms_level', 'is_active')
    search_fields = ('name',)


# ── Mains PYQ ────────────────────────────────────────────

@admin.register(MainsPYQ)
class MainsPYQAdmin(admin.ModelAdmin):
    list_display = ('legacy_code', 'question_preview', 'exam_session', 'paper',
                    'section', 'marks', 'subject', 'difficulty', 'review_status')
    list_filter = ('exam_session', 'paper', 'subject', 'section',
                   'difficulty', 'blooms_level', 'is_up_specific', 'review_status')
    search_fields = ('legacy_code', 'question_text', 'topic_name', 'sub_topic_text',
                      'fact_code', 'tag_code')
    raw_id_fields = ('exam_session', 'subject', 'unit', 'chapter', 'topic', 'part', 'competency')

    @admin.display(description='Question')
    def question_preview(self, obj):
        return obj.question_text[:75] + '...' if len(obj.question_text) > 75 else obj.question_text


# ── Prelims PYQ ─────────────────────────────────────────

class QuestionAppearanceInline(admin.TabularInline):
    model = QuestionAppearance
    extra = 1
    fields = ('exam_name', 'exam_source', 'year', 'question_number', 'is_primary')


@admin.register(PrelimsPYQ)
class PrelimsPYQAdmin(ImportExportModelAdmin):
    resource_classes = [PrelimsPYQResource]
    list_display = ('question_id', 'stem_preview', 'correct_answer', 'exam_source',
                    'year', 'review_status', 'difficulty')
    list_filter = ('exam_source', 'year', 'review_status', 'difficulty',
                   'subject', 'is_free', 'is_active')
    search_fields = ('question_id', 'stem', 'tags', 'concept_cluster')
    raw_id_fields = ('exam_session', 'paper', 'subject', 'unit', 'chapter', 'topic')
    readonly_fields = ('uid', 'stem_length', 'option_avg_length',
                       'times_attempted', 'times_correct', 'avg_time_taken')
    list_per_page = 50
    inlines = [QuestionAppearanceInline]

    @admin.display(description='Question')
    def stem_preview(self, obj):
        return obj.stem[:80] + '...' if len(obj.stem) > 80 else obj.stem


# ── Question Appearance ─────────────────────────────────

@admin.register(QuestionAppearance)
class QuestionAppearanceAdmin(admin.ModelAdmin):
    list_display = ('question', 'exam_name', 'year', 'question_number', 'is_primary')
    list_filter = ('exam_source', 'year', 'is_primary')
    search_fields = ('question__stem', 'question__question_id', 'exam_name')
    list_per_page = 50


# ── Exam Source ────────────────────────────────────────────

@admin.register(ExamSource)
class ExamSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'exam_family', 'exam_stage', 'state', 'is_active')
    list_filter = ('exam_family', 'exam_stage', 'is_active')
    search_fields = ('name', 'short_name')
