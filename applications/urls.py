from django.urls import path
from .views import (
    InstalledAppListCreateView,
    AppPermissionListView,
    AppExecutionLogListView,
)

urlpatterns = [
    path(
        '',
        InstalledAppListCreateView.as_view(),
        name='installed-app-list'
    ),

    path(
        '<int:app_id>/permissions/',
        AppPermissionListView.as_view(),
        name='app-permission-list'
    ),

    path(
        '<int:app_id>/execution-logs/',
        AppExecutionLogListView.as_view(),
        name='app-execution-log-list'
    ),
]
