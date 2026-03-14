"""
PURPOSE: DRF ViewSets and views for the public content API.
USED BY: content/api_urls.py
DEPENDS ON: content/models.py, content/serializers.py, rest_framework
"""

from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from content.models import Chapter, PrelimsPYQ, Subject, Topic
from content.serializers import (
    ChapterSerializer,
    QuestionDetailSerializer,
    QuestionListSerializer,
    SubjectSerializer,
    TopicSerializer,
)


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve subjects with question/chapter counts."""

    queryset = Subject.objects.filter(is_active=True)
    serializer_class = SubjectSerializer
    permission_classes = [AllowAny]
    search_fields = ['name', 'code']


class ChapterViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve chapters, filterable by subject."""

    queryset = Chapter.objects.filter(is_active=True).select_related(
        'unit', 'unit__subject',
    )
    serializer_class = ChapterSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['unit__subject']
    search_fields = ['name', 'code']

    @action(detail=True, methods=['get'])
    def topics(self, request, pk=None):
        """Return all topics for a given chapter."""
        chapter = self.get_object()
        topics = Topic.objects.filter(chapter=chapter, is_active=True)
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """List, retrieve, and interact with prelims questions."""

    queryset = PrelimsPYQ.objects.filter(is_active=True).select_related(
        'subject',
    )
    permission_classes = [AllowAny]
    filterset_fields = ['difficulty', 'year', 'exam_source', 'subject']
    search_fields = ['stem', 'question_id']
    ordering_fields = ['year', 'difficulty', 'question_id']

    def get_serializer_class(self):
        """Use list serializer for list, detail serializer for retrieve."""
        if self.action == 'retrieve':
            return QuestionDetailSerializer
        return QuestionListSerializer

    @action(detail=False, methods=['get'])
    def by_chapter(self, request):
        """Filter questions by chapter code: /questions/by_chapter/?code=FR."""
        code = request.query_params.get('code', '')
        if not code:
            return Response(
                {'error': 'code parameter is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        questions = self.get_queryset().filter(chapter__code=code)
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = QuestionListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = QuestionListSerializer(questions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def check_answer(self, request, pk=None):
        """POST {"answer": "A"} — returns correct/wrong + marks."""
        question = self.get_object()
        student_answer = request.data.get('answer', '').strip().upper()

        if student_answer not in ('A', 'B', 'C', 'D'):
            return Response(
                {'error': 'answer must be A, B, C, or D'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_correct = student_answer == question.correct_answer
        # UPPCS marking: +2.0 for correct, -0.66 for wrong
        marks = 2.0 if is_correct else -0.66

        detail_serializer = QuestionDetailSerializer(question)
        return Response({
            'is_correct': is_correct,
            'marks': marks,
            'your_answer': student_answer,
            'correct_answer': question.correct_answer,
            'question': detail_serializer.data,
        })

    @action(detail=False, methods=['get'])
    def random_set(self, request):
        """Return a random set: /questions/random_set/?count=10&subject=3."""
        count = int(request.query_params.get('count', 10))
        # Cap at 50 to prevent abuse
        count = min(count, 50)
        qs = self.get_queryset()
        subject_id = request.query_params.get('subject')
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        questions = qs.order_by('?')[:count]
        serializer = QuestionListSerializer(questions, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def stats_view(request):
    """Return platform-wide totals and breakdowns."""
    total_questions = PrelimsPYQ.objects.filter(is_active=True).count()
    total_subjects = Subject.objects.filter(is_active=True).count()
    total_chapters = Chapter.objects.filter(is_active=True).count()

    by_subject = list(
        PrelimsPYQ.objects.filter(is_active=True, subject__isnull=False)
        .values('subject__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    by_difficulty = list(
        PrelimsPYQ.objects.filter(is_active=True)
        .values('difficulty')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    return Response({
        'total_questions': total_questions,
        'total_subjects': total_subjects,
        'total_chapters': total_chapters,
        'by_subject': by_subject,
        'by_difficulty': by_difficulty,
    })
