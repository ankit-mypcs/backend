"""
PURPOSE: URL routing for the content REST API.
USED BY: mypcs_project/urls.py (included under /api/)
DEPENDS ON: content/api_views.py, rest_framework.routers
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from content.api_views import (
    ChapterViewSet,
    QuestionViewSet,
    SubjectViewSet,
    stats_view,
)

router = DefaultRouter()
router.register('subjects', SubjectViewSet, basename='subject')
router.register('chapters', ChapterViewSet, basename='chapter')
router.register('questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('stats/', stats_view, name='api-stats'),
    path('', include(router.urls)),
]
