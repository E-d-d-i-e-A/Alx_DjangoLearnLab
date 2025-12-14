Likes and Notifications API Documentation
Overview
This documentation covers the likes system and notifications functionality in the Social Media API.
Base URL
http://localhost:8000/api/
Authentication
All endpoints require authentication using Token Authentication.
Header:
Authorization: Token <your-token-here>
Likes Endpoints
1. Like a Post
Endpoint: POST /api/posts/<int:pk>/like/
Authentication: Required
Description: Like a post. Creates a notification for the post author. Prevents duplicate likes.
URL Parameters:
pk (integer): The ID of the post to like
Example Request:
POST /api/posts/5/like/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (201 Created):
{
    "message": "Post liked successfully",
    "likes_count": 3
}
Error Responses:
400 Bad Request - Already liked:
{
    "error": "You have already liked this post"
}
404 Not Found - Post doesn't exist:
{
    "detail": "Not found."
}
2. Unlike a Post
Endpoint: POST /api/posts/<int:pk>/unlike/
Authentication: Required
Description: Remove your like from a post.
URL Parameters:
pk (integer): The ID of the post to unlike
Example Request:
POST /api/posts/5/unlike/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "message": "Post unliked successfully",
    "likes_count": 2
}
Error Responses:
400 Bad Request - Haven't liked:
{
    "error": "You have not liked this post"
}
404 Not Found - Post doesn't exist:
{
    "detail": "Not found."
}
3. View Post with Likes Information
Endpoint: GET /api/posts/<int:pk>/
Authentication: Not required (but provides more info when authenticated)
Description: Get post details including likes count and whether the current user has liked it.
Example Request:
GET /api/posts/5/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "id": 5,
    "author": "john_doe",
    "author_id": 1,
    "title": "My Awesome Post",
    "content": "This is the content of my post",
    "created_at": "2024-12-14T10:30:00Z",
    "updated_at": "2024-12-14T10:30:00Z",
    "comments": [],
    "comments_count": 0,
    "likes_count": 3,
    "liked_by_user": true
}
Fields:
likes_count: Total number of likes on the post
liked_by_user: Boolean indicating if the authenticated user has liked this post
Notifications Endpoints
1. List All Notifications
Endpoint: GET /api/notifications/
Authentication: Required
Description: Get all notifications for the authenticated user, ordered by most recent first. Unread notifications are marked with "read": false.
Example Request:
GET /api/notifications/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 10,
            "recipient": 1,
            "recipient_username": "john_doe",
            "actor": 2,
            "actor_username": "jane_smith",
            "verb": "liked your post",
            "target_content_type": 8,
            "target_object_id": 5,
            "timestamp": "2024-12-14T15:30:00Z",
            "read": false
        },
        {
            "id": 9,
            "recipient": 1,
            "recipient_username": "john_doe",
            "actor": 3,
            "actor_username": "bob_jones",
            "verb": "started following you",
            "target_content_type": 4,
            "target_object_id": 1,
            "timestamp": "2024-12-14T14:20:00Z",
            "read": true
        },
        {
            "id": 8,
            "recipient": 1,
            "recipient_username": "john_doe",
            "actor": 4,
            "actor_username": "alice_wonder",
            "verb": "commented on your post",
            "target_content_type": 8,
            "target_object_id": 3,
            "timestamp": "2024-12-14T13:15:00Z",
            "read": true
        }
    ]
}
2. Get Unread Notifications Count
Endpoint: GET /api/notifications/unread-count/
Authentication: Required
Description: Get the count of unread notifications for quick display in UI (like a badge).
Example Request:
GET /api/notifications/unread-count/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "unread_count": 3
}
3. Mark Notification as Read
Endpoint: POST /api/notifications/<int:notification_id>/read/
Authentication: Required
Description: Mark a specific notification as read.
URL Parameters:
notification_id (integer): The ID of the notification
Example Request:
POST /api/notifications/10/read/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "message": "Notification marked as read"
}
Error Response (404 Not Found):
{
    "error": "Notification not found"
}
4. Mark All Notifications as Read
Endpoint: POST /api/notifications/read-all/
Authentication: Required
Description: Mark all unread notifications as read for the authenticated user.
Example Request:
POST /api/notifications/read-all/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "message": "All notifications marked as read"
}
Notification Types
The system automatically creates notifications for the following actions:
1. New Follower
Trigger: When someone follows you
Verb: "started following you"
Example:
{
    "actor_username": "jane_smith",
    "verb": "started following you",
    "timestamp": "2024-12-14T14:20:00Z"
}
2. Post Liked
Trigger: When someone likes your post
Verb: "liked your post"
Example:
{
    "actor_username": "bob_jones",
    "verb": "liked your post",
    "target_object_id": 5,
    "timestamp": "2024-12-14T15:30:00Z"
}
3. Post Commented
Trigger: When someone comments on your post
Verb: "commented on your post"
Example:
{
    "actor_username": "alice_wonder",
    "verb": "commented on your post",
    "target_object_id": 3,
    "timestamp": "2024-12-14T13:15:00Z"
}
Models
Like Model
class Like(models.Model):
    user = ForeignKey(User)          # User who liked
    post = ForeignKey(Post)          # Post that was liked
    created_at = DateTimeField()     # When the like was created
    
    # Ensures one user can only like a post once
    unique_together = ('user', 'post')
Notification Model
class Notification(models.Model):
    recipient = ForeignKey(User)              # User receiving notification
    actor = ForeignKey(User)                  # User who performed the action
    verb = CharField()                        # Description of action
    target = GenericForeignKey()              # The object being acted upon
    timestamp = DateTimeField()               # When notification was created
    read = BooleanField(default=False)        # Whether notification has been read
Testing Workflow with Postman
Scenario 1: Like a Post and Check Notifications
Step 1: User 1 Creates a Post
POST /api/posts/
Authorization: Token {token1}
Body: {
    "title": "Check out my post",
    "content": "This is awesome!"
}
Note the post ID (e.g., 5)
Step 2: User 2 Likes the Post
POST /api/posts/5/like/
Authorization: Token {token2}
Step 3: User 1 Checks Notifications
GET /api/notifications/
Authorization: Token {token1}
Expected: Notification showing User 2 liked the post
Step 4: User 1 Checks Unread Count
GET /api/notifications/unread-count/
Authorization: Token {token1}
Expected: {"unread_count": 1}
Step 5: User 1 Marks Notification as Read
POST /api/notifications/1/read/
Authorization: Token {token1}
Step 6: User 2 Unlikes the Post
POST /api/posts/5/unlike/
Authorization: Token {token2}
Scenario 2: Follow, Comment, Like - Multiple Notifications
Step 1: User 2 Follows User 1
POST /api/accounts/follow/1/
Authorization: Token {token2}
Step 2: User 2 Comments on User 1's Post
POST /api/comments/
Authorization: Token {token2}
Body: {
    "post": 5,
    "content": "Great post!"
}
Step 3: User 2 Likes User 1's Post
POST /api/posts/5/like/
Authorization: Token {token2}
Step 4: User 1 Views All Notifications
GET /api/notifications/
Authorization: Token {token1}
Expected: 3 notifications (follow, comment, like)
Step 5: User 1 Marks All as Read
POST /api/notifications/read-all/
Authorization: Token {token1}
Scenario 3: Prevent Duplicate Likes
Step 1: User 2 Likes a Post
POST /api/posts/5/like/
Authorization: Token {token2}
Expected: Success
Step 2: User 2 Tries to Like Again
POST /api/posts/5/like/
Authorization: Token {token2}
Expected: Error - "You have already liked this post"
Step 3: View Post Details
GET /api/posts/5/
Authorization: Token {token2}
Expected: "liked_by_user": true and "likes_count": 1
Database Migrations Required
After creating the new models, run:
# Create notifications app migrations
python manage.py makemigrations notifications

# Update posts app for Like model
python manage.py makemigrations posts

# Apply all migrations
python manage.py migrate
Features Summary
Likes System:
✅ Like Posts - Users can like posts they enjoy
✅ Unlike Posts - Users can remove their likes
✅ Prevent Duplicates - Each user can only like a post once
✅ Like Counts - Posts display total number of likes
✅ User Like Status - Shows if current user has liked a post
✅ Notifications - Post authors get notified when their post is liked
Notifications System:
✅ Auto-Created - Notifications created automatically for key actions
✅ Multiple Types - Supports follows, likes, and comments
✅ Unread Tracking - Distinguishes between read and unread notifications
✅ Unread Count - Quick API to get count of unread notifications
✅ Mark as Read - Individual or bulk marking as read
✅ Chronological Order - Newest notifications shown first
✅ No Self-Notifications - Users don't get notified of their own actions
API Endpoints Summary
Method
Endpoint
Description
Auth
POST
/api/posts/<pk>/like/
Like a post
✅
POST
/api/posts/<pk>/unlike/
Unlike a post
✅
GET
/api/notifications/
List all notifications
✅
GET
/api/notifications/unread-count/
Get unread count
✅
POST
/api/notifications/<id>/read/
Mark notification as read
✅
POST
/api/notifications/read-all/
Mark all as read
✅
Error Handling
Status Code
Description
200 OK
Request successful
201 Created
Like created successfully
400 Bad Request
Duplicate like or haven't liked
401 Unauthorized
Not authenticated
404 Not Found
Post or notification not found
Best Practices
Check Unread Count on App Launch - Show badge with unread count
Mark as Read When Viewed - Mark notifications read when user views them
Periodic Refresh - Poll notifications endpoint every 30-60 seconds
Show Like Status - Display whether user has liked posts
Prevent Duplicate Requests - Disable like button after clicking
Handle Errors Gracefully - Show user-friendly error messages