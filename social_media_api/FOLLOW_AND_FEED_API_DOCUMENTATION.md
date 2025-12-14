Follow and Feed API Documentation
Overview
This documentation covers the user follow system and feed functionality in the Social Media API.
Base URL
http://localhost:8000/api/
Authentication
All endpoints require authentication using Token Authentication.
Header:
Authorization: Token <your-token-here>
Follow Management Endpoints
1. Follow a User
Endpoint: POST /api/accounts/follow/<user_id>/
Authentication: Required
Description: Follow another user by their user ID.
URL Parameters:
user_id (integer): The ID of the user you want to follow
Example Request:
POST /api/accounts/follow/5/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "message": "You are now following john_doe",
    "following": "john_doe"
}
Error Responses:
400 Bad Request - Trying to follow yourself:
{
    "error": "You cannot follow yourself"
}
400 Bad Request - Already following:
{
    "error": "You are already following this user"
}
404 Not Found - User doesn't exist:
{
    "detail": "Not found."
}
2. Unfollow a User
Endpoint: POST /api/accounts/unfollow/<user_id>/
Authentication: Required
Description: Unfollow a user you are currently following.
URL Parameters:
user_id (integer): The ID of the user you want to unfollow
Example Request:
POST /api/accounts/unfollow/5/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "message": "You have unfollowed john_doe",
    "unfollowed": "john_doe"
}
Error Responses:
400 Bad Request - Trying to unfollow yourself:
{
    "error": "You cannot unfollow yourself"
}
400 Bad Request - Not following:
{
    "error": "You are not following this user"
}
404 Not Found - User doesn't exist:
{
    "detail": "Not found."
}
3. List Your Followers
Endpoint: GET /api/accounts/followers/
Authentication: Required
Description: Get a list of all users who are following you.
Example Request:
GET /api/accounts/followers/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "count": 3,
    "followers": [
        {
            "id": 2,
            "username": "jane_smith",
            "bio": "Software developer and tech enthusiast"
        },
        {
            "id": 3,
            "username": "bob_jones",
            "bio": "Photographer | Travel lover"
        },
        {
            "id": 5,
            "username": "alice_wonder",
            "bio": "Writer and blogger"
        }
    ]
}
4. List Users You're Following
Endpoint: GET /api/accounts/following/
Authentication: Required
Description: Get a list of all users you are following.
Example Request:
GET /api/accounts/following/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "count": 2,
    "following": [
        {
            "id": 4,
            "username": "charlie_brown",
            "bio": "Tech blogger and coder"
        },
        {
            "id": 6,
            "username": "david_king",
            "bio": "Entrepreneur | Startup founder"
        }
    ]
}
Feed Endpoint
Get Your Personalized Feed
Endpoint: GET /api/feed/
Authentication: Required
Description: Get a feed of posts from users you follow, ordered by creation date (most recent first).
Query Parameters:
page (integer, optional): Page number for pagination (default: 1)
page_size (integer, optional): Number of posts per page (default: 10, max: 100)
Example Request:
GET /api/feed/?page=1&page_size=10
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Success Response (200 OK):
{
    "count": 25,
    "next": "http://localhost:8000/api/feed/?page=2",
    "previous": null,
    "results": [
        {
            "id": 15,
            "author": "charlie_brown",
            "author_id": 4,
            "title": "Learning Django REST Framework",
            "content": "Just finished building my first API with DRF. Amazing framework!",
            "created_at": "2024-12-14T15:30:00Z",
            "updated_at": "2024-12-14T15:30:00Z",
            "comments": [
                {
                    "id": 23,
                    "post": 15,
                    "author": "jane_smith",
                    "author_id": 2,
                    "content": "Great job! DRF is awesome!",
                    "created_at": "2024-12-14T15:45:00Z",
                    "updated_at": "2024-12-14T15:45:00Z"
                }
            ],
            "comments_count": 1
        },
        {
            "id": 14,
            "author": "david_king",
            "author_id": 6,
            "title": "New Product Launch",
            "content": "Excited to announce our new product going live next week!",
            "created_at": "2024-12-14T14:20:00Z",
            "updated_at": "2024-12-14T14:20:00Z",
            "comments": [],
            "comments_count": 0
        }
    ]
}
Empty Feed Response (200 OK):
If you're not following anyone or they haven't posted yet:
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
User Model Changes
Updated CustomUser Model Fields
The CustomUser model has been updated with the following fields:
username (string): Unique username
email (string): User's email address
bio (text): User biography (max 500 characters)
profile_picture (image): Profile picture URL
followers (ManyToMany): Users who follow this user
following (ManyToMany): Users this user follows (reverse relation)
Relationship Structure
# User A follows User B
user_a.following.add(user_b)  # User A is now following User B
user_b.followers.all()         # Will include User A

# User A unfollows User B
user_a.following.remove(user_b)
Testing Workflow with Postman
Scenario 1: Follow Users and View Feed
Step 1: Register/Login as User 1
POST /api/accounts/register/
Body: {
    "username": "user1",
    "email": "user1@example.com",
    "password": "password123"
}
Save the token: token1
Step 2: Register/Login as User 2
POST /api/accounts/register/
Body: {
    "username": "user2",
    "email": "user2@example.com",
    "password": "password123"
}
Save the token: token2
Step 3: User 2 Creates a Post
POST /api/posts/
Authorization: Token {token2}
Body: {
    "title": "Hello World",
    "content": "This is my first post!"
}
Step 4: User 1 Follows User 2
POST /api/accounts/follow/2/
Authorization: Token {token1}
Step 5: User 1 Views Feed
GET /api/feed/
Authorization: Token {token1}
Expected: User 2's post appears in User 1's feed
Step 6: User 1 Unfollows User 2
POST /api/accounts/unfollow/2/
Authorization: Token {token1}
Step 7: User 1 Views Feed Again
GET /api/feed/
Authorization: Token {token1}
Expected: Feed is now empty
Scenario 2: Check Followers and Following
Step 1: User 1 Follows Multiple Users
POST /api/accounts/follow/2/
POST /api/accounts/follow/3/
POST /api/accounts/follow/4/
Authorization: Token {token1}
Step 2: Check Who User 1 is Following
GET /api/accounts/following/
Authorization: Token {token1}
Step 3: Login as User 2 and Check Followers
GET /api/accounts/followers/
Authorization: Token {token2}
Expected: User 1 appears in User 2's followers list
Common Use Cases
1. Building a Social Network
Users register and create profiles
Users follow interesting accounts
Feed shows updates from followed users
Users interact through comments
2. Content Discovery
Users browse posts (GET /api/posts/)
Users find interesting authors
Users follow those authors
Future posts appear in their feed
3. Social Interactions
Check who follows you (GET /api/accounts/followers/)
Check who you follow (GET /api/accounts/following/)
Manage following list (follow/unfollow)
Stay updated via feed
Error Handling Summary
Status Code
Description
200 OK
Request successful
400 Bad Request
Invalid request (e.g., following yourself, already following)
401 Unauthorized
Not authenticated or invalid token
404 Not Found
User or resource not found
Database Migrations Required
After updating the models, run:
python manage.py makemigrations accounts
python manage.py migrate
This creates the necessary database tables for the follow relationships.
Features Summary
✅ Follow/Unfollow System: Users can follow and unfollow each other
✅ Relationship Management: View followers and following lists
✅ Personalized Feed: See posts only from followed users
✅ Chronological Order: Feed shows most recent posts first
✅ Pagination: Feed supports pagination for large datasets
✅ Protection: Cannot follow yourself, proper error handling
✅ Authentication: All endpoints require authentication
✅ Permissions: Users can only modify their own follow relationships