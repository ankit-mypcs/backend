"""
content/views.py — DRF ViewSets for MYPCS API
"""
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from content.models import (
    Chapter, Fact, Site, TimelineEvent, GlossaryTerm,
    ExamIntelEntry, ComparisonMatrix, Visual, Exercise,
    PrelimsPYQ, Topic,
)
from content.serializers import (
    ChapterListSerializer, ChapterDetailSerializer,
    FactSerializer, SiteSerializer, TimelineSerializer,
    GlossarySerializer, ExamIntelSerializer, ConceptMatrixSerializer,
    VisualSerializer, ExerciseSerializer,
    PrelimsListSerializer, PrelimsDetailSerializer,
    StatsSerializer,
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
    /api/questions/         → list (filterable by chapter, year, difficulty)
    /api/questions/{id}/    → detail with options + answer
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
