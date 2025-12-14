from django.urls import path
from .views import (
    NotificationListView,
    mark_notification_read,
    mark_all_notifications_read,
    unread_notifications_count
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:notification_id>/read/', mark_notification_read, name='mark-notification-read'),
    path('read-all/', mark_all_notifications_read, name='mark-all-read'),
    path('unread-count/', unread_notifications_count, name='unread-count'),
]