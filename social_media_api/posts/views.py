from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author
        return obj.author == request.user


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        
        # Create notification for post author
        from notifications.models import Notification
        post = comment.post
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb='commented on your post',
                target=post
            )


class FeedView(generics.ListAPIView):
    """
    View that generates a feed based on posts from users that the current user follows.
    Returns posts ordered by creation date, showing the most recent posts at the top.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        
        # Get users that the current user is following
        following_users = user.following.all()
        
        # Return posts from followed users, ordered by creation date (newest first)
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """
    Like a post. Prevents duplicate likes and creates a notification.
    """
    post = generics.get_object_or_404(Post, pk=pk)
    
    # Check if user already liked the post
    if Like.objects.filter(user=request.user, post=post).exists():
        return Response(
            {'error': 'You have already liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create the like
    like = Like.objects.create(user=request.user, post=post)
    
    # Create notification for post author (don't notify if liking own post)
    if post.author != request.user:
        from notifications.models import Notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )
    
    return Response(
        {
            'message': 'Post liked successfully',
            'likes_count': post.likes.count()
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """
    Unlike a post. Removes the like if it exists.
    """
    post = generics.get_object_or_404(Post, pk=pk)
    
    # Check if like exists
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        
        return Response(
            {
                'message': 'Post unliked successfully',
                'likes_count': post.likes.count()
            },
            status=status.HTTP_200_OK
        )
    except Like.DoesNotExist:
        return Response(
            {'error': 'You have not liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )