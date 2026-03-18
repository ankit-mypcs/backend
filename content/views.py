"""
content/views.py — DRF ViewSets for MYPCS API
"""
from django.db import models
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from content.models import (
    Subject, Chapter, Fact, Site, TimelineEvent, GlossaryTerm,
    ExamIntelEntry, ComparisonMatrix, Visual, Exercise,
    PrelimsPYQ, Topic,
)
from content.serializers import (
    SubjectSerializer,
    ChapterListSerializer, ChapterDetailSerializer,
    FactSerializer, SiteSerializer, TimelineSerializer,
    GlossarySerializer, ExamIntelSerializer, ConceptMatrixSerializer,
    VisualSerializer, ExerciseSerializer,
    PrelimsListSerializer, PrelimsDetailSerializer,
    StatsSerializer,
)


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /api/subjects/ → list with question_count and chapter_count
    """
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.filter(is_active=True).annotate(
            question_count=Count('prelims_pyqs', distinct=True),
            chapter_count=Count(
                'parts__units__chapters',
                filter=models.Q(parts__units__chapters__is_active=True),
                distinct=True,
            ),
        )


class ChapterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /api/chapters/          → list (with counts)
    /api/chapters/{slug}/   → detail (with topic tree)
    + actions: facts, sites, timeline, terms, exam-intel, concepts, visuals, exercises
    """
    lookup_field = 'slug'

    def get_queryset(self):
        qs = Chapter.objects.filter(is_active=True).select_related(
            'unit', 'unit__part', 'unit__part__subject',
        )
        if self.action == 'list':
            qs = qs.annotate(
                fact_count=Count('facts'),
                site_count=Count('sites'),
                pyq_count=Count('prelims_pyqs'),
            )
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChapterDetailSerializer
        return ChapterListSerializer

    @action(detail=True, methods=['get'])
    def facts(self, request, slug=None):
        chapter = self.get_object()
        qs = chapter.facts.select_related('topic', 'sub_topic').prefetch_related('state_relevance')
        sheet = request.query_params.get('sheet')
        if sheet:
            qs = qs.filter(source_sheet=sheet)
        topic = request.query_params.get('topic')
        if topic:
            qs = qs.filter(topic__name__icontains=topic)
        return Response(FactSerializer(qs, many=True).data)

    @action(detail=True, methods=['get'])
    def sites(self, request, slug=None):
        chapter = self.get_object()
        qs = chapter.sites.select_related('topic')
        return Response(SiteSerializer(qs, many=True).data)

    @action(detail=True, methods=['get'])
    def timeline(self, request, slug=None):
        chapter = self.get_object()
        qs = chapter.timeline_events.select_related('topic')
        return Response(TimelineSerializer(qs, many=True).data)

    @action(detail=True, methods=['get'])
    def terms(self, request, slug=None):
        chapter = self.get_object()
        qs = chapter.glossary_terms.select_related('topic')
        return Response(GlossarySerializer(qs, many=True).data)

    @action(detail=True, url_path='exam-intel', methods=['get'])
    def exam_intel(self, request, slug=None):
        chapter = self.get_object()
        qs = chapter.exam_intel_entries.select_related('topic')
        return Response(ExamIntelSerializer(qs, many=True).data)

    @action(detail=True, methods=['get'])
    def concepts(self, request, slug=None):
        chapter = self.get_object()
        qs = chapter.comparison_matrices.all()
        return Response(ConceptMatrixSerializer(qs, many=True).data)

    @action(detail=True, methods=['get'])
    def visuals(self, request, slug=None):
        chapter = self.get_object()
        qs = chapter.visuals.select_related('topic')
        return Response(VisualSerializer(qs, many=True).data)

    @action(detail=True, methods=['get'])
    def exercises(self, request, slug=None):
        chapter = self.get_object()
        qs = chapter.exercises.select_related('topic')
        return Response(ExerciseSerializer(qs, many=True).data)


class PrelimsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /api/questions/                → list (filterable by chapter, year, difficulty)
    /api/questions/{id}/           → detail with options + answer
    /api/questions/random_set/     → random set of N questions
    /api/questions/{id}/check_answer/ → submit answer, get marks
    """

    def get_queryset(self):
        qs = PrelimsPYQ.objects.filter(
            is_active=True,
        ).select_related('chapter', 'topic', 'subject')

        chapter = self.request.query_params.get('chapter')
        if chapter:
            qs = qs.filter(chapter__slug=chapter)
        year = self.request.query_params.get('year')
        if year:
            qs = qs.filter(year=year)
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            qs = qs.filter(difficulty=difficulty)

        status_filter = self.request.query_params.get('status', 'draft')
        if status_filter != 'all':
            qs = qs.filter(review_status=status_filter)

        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PrelimsDetailSerializer
        return PrelimsListSerializer

    @action(detail=False, methods=['get'], url_path='random_set')
    def random_set(self, request):
        """Return N random questions with complete options."""
        count = int(request.query_params.get('count', 10))
        count = min(count, 50)  # cap at 50

        qs = PrelimsPYQ.objects.filter(
            is_active=True,
            review_status='draft',
        ).exclude(
            option_a='',
        ).select_related('chapter', 'topic', 'subject')

        # Filter by subject if provided
        subject = request.query_params.get('subject')
        if subject:
            qs = qs.filter(subject_id=subject)

        questions = qs.order_by('?')[:count]
        return Response(PrelimsListSerializer(questions, many=True).data)

    @action(detail=True, methods=['post'], url_path='check_answer')
    def check_answer(self, request, pk=None):
        """Submit an answer, return correctness and marks."""
        question = self.get_object()
        answer = request.data.get('answer', '').upper()

        is_correct = (answer == question.correct_answer)
        marks = 2.0 if is_correct else -0.66

        return Response({
            'is_correct': is_correct,
            'marks': marks,
            'your_answer': answer,
            'correct_answer': question.correct_answer,
            'question': PrelimsDetailSerializer(question).data,
        })


@api_view(['GET'])
def stats_view(request):
    """Dashboard stats — /api/stats/"""
    data = {
        'chapters': Chapter.objects.filter(is_active=True).count(),
        'topics': Topic.objects.count(),
        'facts': Fact.objects.count(),
        'sites': Site.objects.count(),
        'timeline_events': TimelineEvent.objects.count(),
        'glossary_terms': GlossaryTerm.objects.count(),
        'visuals': Visual.objects.count(),
        'exercises': Exercise.objects.count(),
        'prelims_pyqs': PrelimsPYQ.objects.count(),
        'prelims_complete': PrelimsPYQ.objects.filter(review_status='draft').count(),
    }
    return Response(StatsSerializer(data).data)
