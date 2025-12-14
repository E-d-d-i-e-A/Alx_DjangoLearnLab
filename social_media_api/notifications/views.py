from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    View to list all notifications for the authenticated user.
    Unread notifications are shown prominently.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return notifications for the current user, ordered by timestamp (newest first)
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    """
    Mark a specific notification as read
    """
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.read = True
        notification.save()
        return Response(
            {'message': 'Notification marked as read'},
            status=status.HTTP_200_OK
        )
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """
    Mark all notifications as read for the authenticated user
    """
    Notification.objects.filter(recipient=request.user, read=False).update(read=True)
    return Response(
        {'message': 'All notifications marked as read'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_notifications_count(request):
    """
    Get the count of unread notifications
    """
    count = Notification.objects.filter(recipient=request.user, read=False).count()
    return Response(
        {'unread_count': count},
        status=status.HTTP_200_OK
    )