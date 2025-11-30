from django.urls import path
from .views import create_task, analyze_tasks, suggest_tasks

urlpatterns = [
    path("tasks/create/", create_task),
    path("tasks/analyze/", analyze_tasks),
    path("tasks/suggest/", suggest_tasks),
]
