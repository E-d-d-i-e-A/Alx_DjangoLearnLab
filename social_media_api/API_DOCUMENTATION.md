Posts and Comments API Documentation
Base URL
http://localhost:8000/api/
Authentication
All POST, PUT, PATCH, and DELETE requests require authentication using Token Authentication.
Add the following header to authenticated requests:
Authorization: Token <your-token-here>
Posts Endpoints
1. List All Posts
Endpoint: GET /api/posts/
Authentication: Not required (read-only)
Query Parameters:
page: Page number (default: 1)
page_size: Results per page (default: 10, max: 100)
search: Search by title or content
Example Request:
GET /api/posts/?search=django&page=1&page_size=10
Example Response:
{
    "count": 25,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": "john_doe",
            "author_id": 1,
            "title": "My First Post",
            "content": "This is my first post content",
            "created_at": "2024-12-14T10:30:00Z",
            "updated_at": "2024-12-14T10:30:00Z",
            "comments": [],
            "comments_count": 0
        }
    ]
}
2. Create a Post
Endpoint: POST /api/posts/
Authentication: Required
Request Body:
{
    "title": "My New Post",
    "content": "This is the content of my post"
}
Example Response:
{
    "id": 2,
    "author": "john_doe",
    "author_id": 1,
    "title": "My New Post",
    "content": "This is the content of my post",
    "created_at": "2024-12-14T11:00:00Z",
    "updated_at": "2024-12-14T11:00:00Z",
    "comments": [],
    "comments_count": 0
}
3. Retrieve a Single Post
Endpoint: GET /api/posts/{id}/
Authentication: Not required
Example Request:
GET /api/posts/1/
Example Response:
{
    "id": 1,
    "author": "john_doe",
    "author_id": 1,
    "title": "My First Post",
    "content": "This is my first post content",
    "created_at": "2024-12-14T10:30:00Z",
    "updated_at": "2024-12-14T10:30:00Z",
    "comments": [
        {
            "id": 1,
            "post": 1,
            "author": "jane_smith",
            "author_id": 2,
            "content": "Great post!",
            "created_at": "2024-12-14T10:35:00Z",
            "updated_at": "2024-12-14T10:35:00Z"
        }
    ],
    "comments_count": 1
}
4. Update a Post
Endpoint: PUT /api/posts/{id}/ or PATCH /api/posts/{id}/
Authentication: Required (must be the author)
Request Body (PUT - all fields required):
{
    "title": "Updated Title",
    "content": "Updated content"
}
Request Body (PATCH - partial update):
{
    "title": "Updated Title"
}
Example Response:
{
    "id": 1,
    "author": "john_doe",
    "author_id": 1,
    "title": "Updated Title",
    "content": "Updated content",
    "created_at": "2024-12-14T10:30:00Z",
    "updated_at": "2024-12-14T11:30:00Z",
    "comments": [],
    "comments_count": 0
}
5. Delete a Post
Endpoint: DELETE /api/posts/{id}/
Authentication: Required (must be the author)
Example Request:
DELETE /api/posts/1/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Response: 204 No Content
Comments Endpoints
1. List All Comments
Endpoint: GET /api/comments/
Authentication: Not required
Query Parameters:
page: Page number
page_size: Results per page
Example Response:
{
    "count": 15,
    "next": "http://localhost:8000/api/comments/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "post": 1,
            "author": "jane_smith",
            "author_id": 2,
            "content": "Great post!",
            "created_at": "2024-12-14T10:35:00Z",
            "updated_at": "2024-12-14T10:35:00Z"
        }
    ]
}
2. Create a Comment
Endpoint: POST /api/comments/
Authentication: Required
Request Body:
{
    "post": 1,
    "content": "This is my comment"
}
Example Response:
{
    "id": 2,
    "post": 1,
    "author": "john_doe",
    "author_id": 1,
    "content": "This is my comment",
    "created_at": "2024-12-14T11:00:00Z",
    "updated_at": "2024-12-14T11:00:00Z"
}
3. Retrieve a Single Comment
Endpoint: GET /api/comments/{id}/
Authentication: Not required
Example Response:
{
    "id": 1,
    "post": 1,
    "author": "jane_smith",
    "author_id": 2,
    "content": "Great post!",
    "created_at": "2024-12-14T10:35:00Z",
    "updated_at": "2024-12-14T10:35:00Z"
}
4. Update a Comment
Endpoint: PUT /api/comments/{id}/ or PATCH /api/comments/{id}/
Authentication: Required (must be the author)
Request Body:
{
    "content": "Updated comment text"
}
Example Response:
{
    "id": 1,
    "post": 1,
    "author": "jane_smith",
    "author_id": 2,
    "content": "Updated comment text",
    "created_at": "2024-12-14T10:35:00Z",
    "updated_at": "2024-12-14T11:40:00Z"
}
5. Delete a Comment
Endpoint: DELETE /api/comments/{id}/
Authentication: Required (must be the author)
Response: 204 No Content
Error Responses
400 Bad Request
{
    "title": ["This field is required."]
}
401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
403 Forbidden
{
    "detail": "You do not have permission to perform this action."
}
404 Not Found
{
    "detail": "Not found."
}
Postman Testing Examples
Test 1: Create a Post
Method: POST
URL: http://localhost:8000/api/posts/
Headers:
Authorization: Token <your-token>
Content-Type: application/json
Body (raw JSON):
{
    "title": "Test Post",
    "content": "This is a test post"
}
Test 2: Search Posts
Method: GET
URL: http://localhost:8000/api/posts/?search=test
Headers: None required
Test 3: Add Comment to Post
Method: POST
URL: http://localhost:8000/api/comments/
Headers:
Authorization: Token <your-token>
Content-Type: application/json
Body (raw JSON):
{
    "post": 1,
    "content": "Nice post!"
}
Test 4: Update Your Own Post
Method: PATCH
URL: http://localhost:8000/api/posts/1/
Headers:
Authorization: Token <your-token>
Content-Type: application/json
Body (raw JSON):
{
    "title": "Updated Title"
}
Test 5: Try to Update Someone Else's Post (Should Fail)
Same as Test 4, but with a different user's token
Expected Response: 403 Forbidden
Features Summary
✅ Pagination: All list endpoints support pagination (10 items per page by default)
✅ Search/Filtering: Posts can be searched by title or content using ?search= parameter
✅ Permissions: Only authors can edit/delete their own posts and comments
✅ Nested Data: Post detail includes all associated comments
✅ Timestamps: Automatic created_at and updated_at tracking