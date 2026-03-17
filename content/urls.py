"""
content/urls.py — API URL routing
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from content.views import ChapterViewSet, PrelimsViewSet, stats_view

router = DefaultRouter()
router.register(r'chapters', ChapterViewSet, basename='chapter')
router.register(r'questions', PrelimsViewSet, basename='question')

urlpatterns = [
    path('stats/', stats_view, name='stats'),
    path('', include(router.urls)),
]
