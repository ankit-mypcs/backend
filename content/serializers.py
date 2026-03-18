"""
content/serializers.py — DRF serializers for MYPCS API
"""
from rest_framework import serializers
from content.models import (
    Subject, Part, Unit, Chapter, Topic, SubTopic,
    Fact, Site, TimelineEvent, GlossaryTerm,
    ExamIntelEntry, ComparisonMatrix, Visual, Exercise,
    PrelimsPYQ, State, Exam, ExamSession, Paper,
)


# ── Exam ────────────────────────────────────

class ExamListSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', default='', read_only=True)
    state_code = serializers.CharField(source='state.code', default='', read_only=True)
    pyq_count = serializers.IntegerField(read_only=True)
    session_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id', 'name', 'short_name', 'slug',
            'state_name', 'state_code', 'description',
            'is_target_exam', 'is_active',
            'pyq_count', 'session_count',
        ]


class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = [
            'id', 'name', 'short_name', 'slug', 'exam_stage',
            'total_marks', 'total_questions', 'duration_minutes',
            'paper_type', 'is_qualifying', 'negative_marking',
        ]


class ExamSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSession
        fields = [
            'id', 'year', 'prelims_date', 'mains_date',
            'total_questions_prelims', 'positive_marks_prelims',
            'negative_marks_prelims',
            'cutoff_prelims_general', 'cutoff_prelims_obc',
            'cutoff_prelims_sc', 'cutoff_prelims_st',
            'students_applied', 'students_final_selected',
            'posts_advertised',
        ]


class ExamDetailSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', default='', read_only=True)
    state_code = serializers.CharField(source='state.code', default='', read_only=True)
    papers = PaperSerializer(many=True, read_only=True)
    sessions = ExamSessionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id', 'name', 'short_name', 'slug',
            'state_name', 'state_code', 'description',
            'is_target_exam', 'is_active',
            'papers', 'sessions',
        ]


# ── Subject ──────────────────────────────────

class SubjectSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)
    chapter_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'code', 'slug', 'icon',
            'question_count', 'chapter_count',
        ]


# ── Taxonomy ─────────────────────────────────

class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = ['id', 'name', 'sort_order']


class TopicSerializer(serializers.ModelSerializer):
    subtopics = SubTopicSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug', 'sort_order', 'subtopics']


class ChapterListSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    part_name = serializers.CharField(source='unit.part.name', read_only=True)
    subject_name = serializers.CharField(source='unit.part.subject.name', read_only=True)
    fact_count = serializers.IntegerField(read_only=True)
    site_count = serializers.IntegerField(read_only=True)
    pyq_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chapter
        fields = [
            'id', 'name', 'slug', 'chapter_number', 'sort_order',
            'unit_name', 'part_name', 'subject_name',
            'fact_count', 'site_count', 'pyq_count', 'is_active',
        ]


class ChapterDetailSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    part_name = serializers.CharField(source='unit.part.name', read_only=True)
    subject_name = serializers.CharField(source='unit.part.subject.name', read_only=True)
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = [
            'id', 'name', 'slug', 'chapter_number', 'sort_order',
            'unit_name', 'part_name', 'subject_name',
            'topics', 'is_active',
        ]


# ── Content ──────────────────────────────────

class FactSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', default='', read_only=True)
    sub_topic_name = serializers.CharField(source='sub_topic.name', default='', read_only=True)
    state_tags = serializers.SerializerMethodField()

    class Meta:
        model = Fact
        fields = [
            'id', 'text', 'citation', 'source_sheet', 'sort_order',
            'topic_name', 'sub_topic_name', 'state_tags',
        ]

    def get_state_tags(self, obj):
        return list(obj.state_relevance.values_list('code', flat=True))


class SiteSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', default='', read_only=True)

    class Meta:
        model = Site
        fields = [
            'id', 'name', 'state_region', 'period', 'key_findings',
            'citation', 'topic_name',
        ]


class TimelineSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', default='', read_only=True)

    class Meta:
        model = TimelineEvent
        fields = ['id', 'date_text', 'event', 'citation', 'sort_order', 'topic_name']


class GlossarySerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryTerm
        fields = ['id', 'term', 'definition', 'citation']


class ExamIntelSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', default='', read_only=True)

    class Meta:
        model = ExamIntelEntry
        fields = ['id', 'category', 'detail', 'citation', 'topic_name']


class ConceptMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComparisonMatrix
        fields = ['id', 'title', 'parameters', 'columns', 'data', 'citation']


class VisualSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', default='', read_only=True)

    class Meta:
        model = Visual
        fields = ['id', 'ref_code', 'description', 'source_book', 'topic_name']


class ExerciseSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', default='', read_only=True)

    class Meta:
        model = Exercise
        fields = ['id', 'exercise_type', 'question', 'source', 'topic_name']


# ── PYQ ──────────────────────────────────────

class PrelimsListSerializer(serializers.ModelSerializer):
    chapter_name = serializers.CharField(source='chapter.name', default='', read_only=True)
    topic_name = serializers.CharField(source='topic.name', default='', read_only=True)
    subject_name = serializers.CharField(source='subject.name', default='', read_only=True)
    exam_name = serializers.CharField(source='exam.short_name', default='', read_only=True)
    exam_slug = serializers.CharField(source='exam.slug', default='', read_only=True)

    class Meta:
        model = PrelimsPYQ
        fields = [
            'id', 'question_id', 'stem',
            'option_a', 'option_b', 'option_c', 'option_d',
            'year', 'exam_source', 'exam_name', 'exam_slug', 'difficulty',
            'subject_name', 'chapter_name', 'topic_name',
            'review_status', 'is_active',
        ]


class PrelimsDetailSerializer(serializers.ModelSerializer):
    chapter_name = serializers.CharField(source='chapter.name', default='', read_only=True)
    chapter_slug = serializers.CharField(source='chapter.slug', default='', read_only=True)
    topic_name = serializers.CharField(source='topic.name', default='', read_only=True)

    class Meta:
        model = PrelimsPYQ
        fields = [
            'id', 'uid', 'question_id', 'stem',
            'option_a', 'option_b', 'option_c', 'option_d',
            'correct_answer', 'explanation',
            'year', 'exam_source', 'difficulty', 'blooms_level',
            'concept_cluster', 'tags', 'repeat_count',
            'chapter_name', 'chapter_slug', 'topic_name',
            'review_status', 'is_active',
        ]


# ── Stats ────────────────────────────────────

class StatsSerializer(serializers.Serializer):
    chapters = serializers.IntegerField()
    topics = serializers.IntegerField()
    facts = serializers.IntegerField()
    sites = serializers.IntegerField()
    timeline_events = serializers.IntegerField()
    glossary_terms = serializers.IntegerField()
    visuals = serializers.IntegerField()
    exercises = serializers.IntegerField()
    prelims_pyqs = serializers.IntegerField()
    prelims_complete = serializers.IntegerField()
