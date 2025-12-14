from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            'user': UserRegistrationSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user by their user_id
    """
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # Check if trying to follow yourself
    if user_to_follow == request.user:
        return Response(
            {'error': 'You cannot follow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if already following
    if request.user.following.filter(id=user_id).exists():
        return Response(
            {'error': 'You are already following this user'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Add to following
    request.user.following.add(user_to_follow)
    
    return Response(
        {
            'message': f'You are now following {user_to_follow.username}',
            'following': user_to_follow.username
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user by their user_id
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    # Check if trying to unfollow yourself
    if user_to_unfollow == request.user:
        return Response(
            {'error': 'You cannot unfollow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if not following
    if not request.user.following.filter(id=user_id).exists():
        return Response(
            {'error': 'You are not following this user'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Remove from following
    request.user.following.remove(user_to_unfollow)
    
    return Response(
        {
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'unfollowed': user_to_unfollow.username
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_followers(request):
    """
    List all followers of the current user
    """
    followers = request.user.followers.all()
    followers_data = [
        {
            'id': user.id,
            'username': user.username,
            'bio': user.bio
        }
        for user in followers
    ]
    
    return Response({
        'count': followers.count(),
        'followers': followers_data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_following(request):
    """
    List all users the current user is following
    """
    following = request.user.following.all()
    following_data = [
        {
            'id': user.id,
            'username': user.username,
            'bio': user.bio
        }
        for user in following
    ]
    
    return Response({
        'count': following.count(),
        'following': following_data
    }, status=status.HTTP_200_OK)