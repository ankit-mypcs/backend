"""
PURPOSE: DRF serializers for the content API.
USED BY: content/api_views.py
DEPENDS ON: content/models.py, rest_framework
"""

from rest_framework import serializers

from content.models import (
    Chapter, PrelimsPYQ, QuestionAppearance, Subject, Topic,
)


class SubjectSerializer(serializers.ModelSerializer):
    """Read-only serializer for Subject with computed counts."""

    question_count = serializers.SerializerMethodField()
    chapter_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'name_hi', 'code', 'slug',
            'question_count', 'chapter_count',
        ]

    def get_question_count(self, subject):
        """Count prelims questions linked to this subject."""
        return subject.prelims_pyqs.count()

    def get_chapter_count(self, subject):
        """Count chapters across all units of this subject."""
        return Chapter.objects.filter(unit__subject=subject).count()


class ChapterSerializer(serializers.ModelSerializer):
    """Read-only serializer for Chapter with parent names."""

    subject_name = serializers.SerializerMethodField()
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chapter
        fields = [
            'id', 'name', 'name_hi', 'code', 'slug',
            'subject_name', 'unit_name', 'question_count',
        ]

    def get_subject_name(self, chapter):
        """Return the subject name via unit -> subject."""
        return chapter.unit.subject.name


class TopicSerializer(serializers.ModelSerializer):
    """Read-only serializer for Topic."""

    class Meta:
        model = Topic
        fields = ['id', 'name', 'name_hi', 'slug', 'sort_order']


class AppearanceSerializer(serializers.ModelSerializer):
    """Read-only serializer for QuestionAppearance."""

    class Meta:
        model = QuestionAppearance
        fields = ['exam_source', 'exam_name', 'year', 'is_primary']


class QuestionListSerializer(serializers.ModelSerializer):
    """List view — NO correct_answer (what students see before answering)."""

    subject_name = serializers.CharField(
        source='subject.name', read_only=True, default='',
    )

    class Meta:
        model = PrelimsPYQ
        fields = [
            'id', 'question_id', 'stem',
            'option_a', 'option_b', 'option_c', 'option_d',
            'difficulty', 'year', 'exam_source',
            'subject_name',
        ]


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Detail view — WITH correct_answer + explanations + appearances."""

    subject_name = serializers.CharField(
        source='subject.name', read_only=True, default='',
    )
    appearances = AppearanceSerializer(many=True, read_only=True)

    class Meta:
        model = PrelimsPYQ
        fields = [
            'id', 'question_id', 'stem', 'stem_hi',
            'option_a', 'option_b', 'option_c', 'option_d',
            'correct_answer',
            'explanation', 'explanation_hi',
            'teaching_note', 'mnemonic', 'common_mistake', 'exam_tip',
            'difficulty', 'year', 'exam_source', 'tags',
            'blooms_level', 'repeat_count',
            'subject_name', 'appearances',
        ]


class StatsSerializer(serializers.Serializer):
    """Platform-wide statistics (no model backing)."""

    total_questions = serializers.IntegerField()
    total_subjects = serializers.IntegerField()
    total_chapters = serializers.IntegerField()
    by_subject = serializers.ListField()
    by_difficulty = serializers.ListField()
