from django.urls import path
from .views import course_list_view, course_detail_view, lesson_detail_view

urlpatterns = [
    path('', course_list_view),
    path('<slug:course_id>/', course_detail_view),
    path('<slug:course_id>/lessons/<slug:lesson_id>/', lesson_detail_view),
]
