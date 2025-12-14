from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'recipient_username', 'actor', 'actor_username', 
                  'verb', 'target_content_type', 'target_object_id', 'timestamp', 'read']
        read_only_fields = ['id', 'recipient', 'actor', 'timestamp']