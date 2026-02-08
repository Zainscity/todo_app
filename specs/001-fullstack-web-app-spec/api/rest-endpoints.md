# REST API Contract

## Endpoint Specifications

### GET /api/{user_id}/tasks
- **Description**: Retrieve all tasks for the specified user
- **Method**: GET
- **Authentication**: Required (valid JWT token)
- **Path Parameters**:
  - `{user_id}`: User identifier (must match authenticated user)
- **Query Parameters**:
  - `limit`: Number of tasks to return (default: 50, max: 100)
  - `offset`: Number of tasks to skip (for pagination)
  - `status`: Filter by completion status ("all", "completed", "pending")
- **Request Headers**:
  - `Authorization: Bearer {jwt_token}`
- **Response**:
  - `200 OK`: Array of task objects
  - `401 Unauthorized`: Invalid or missing authentication
  - `403 Forbidden`: User attempting to access another user's tasks
  - `404 Not Found`: User ID does not exist
- **Response Body**:
  ```json
  [
    {
      "id": "uuid-string",
      "user_id": "uuid-string",
      "title": "Task title",
      "description": "Optional task description",
      "completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
  ```

### POST /api/{user_id}/tasks
- **Description**: Create a new task for the specified user
- **Method**: POST
- **Authentication**: Required (valid JWT token)
- **Path Parameters**:
  - `{user_id}`: User identifier (must match authenticated user)
- **Request Headers**:
  - `Authorization: Bearer {jwt_token}`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "Task title (required)",
    "description": "Optional task description"
  }
  ```
- **Response**:
  - `201 Created`: Task successfully created
  - `400 Bad Request`: Invalid request body or missing required fields
  - `401 Unauthorized`: Invalid or missing authentication
  - `403 Forbidden`: User attempting to create task for another user
  - `404 Not Found`: User ID does not exist
- **Response Body**:
  ```json
  {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "title": "Task title",
    "description": "Optional task description",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
  ```

### GET /api/{user_id}/tasks/{id}
- **Description**: Retrieve a specific task for the specified user
- **Method**: GET
- **Authentication**: Required (valid JWT token)
- **Path Parameters**:
  - `{user_id}`: User identifier (must match authenticated user)
  - `{id}`: Task identifier
- **Request Headers**:
  - `Authorization: Bearer {jwt_token}`
- **Response**:
  - `200 OK`: Task object found and returned
  - `401 Unauthorized`: Invalid or missing authentication
  - `403 Forbidden`: User attempting to access another user's task
  - `404 Not Found`: Task or user ID does not exist
- **Response Body**:
  ```json
  {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "title": "Task title",
    "description": "Optional task description",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
  ```

### PUT /api/{user_id}/tasks/{id}
- **Description**: Update an existing task for the specified user
- **Method**: PUT
- **Authentication**: Required (valid JWT token)
- **Path Parameters**:
  - `{user_id}`: User identifier (must match authenticated user)
  - `{id}`: Task identifier
- **Request Headers**:
  - `Authorization: Bearer {jwt_token}`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "title": "Updated task title",
    "description": "Updated task description"
  }
  ```
- **Response**:
  - `200 OK`: Task successfully updated
  - `400 Bad Request`: Invalid request body or missing required fields
  - `401 Unauthorized`: Invalid or missing authentication
  - `403 Forbidden`: User attempting to update another user's task
  - `404 Not Found`: Task or user ID does not exist
- **Response Body**:
  ```json
  {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z"
  }
  ```

### DELETE /api/{user_id}/tasks/{id}
- **Description**: Delete a specific task for the specified user
- **Method**: DELETE
- **Authentication**: Required (valid JWT token)
- **Path Parameters**:
  - `{user_id}`: User identifier (must match authenticated user)
  - `{id}`: Task identifier
- **Request Headers**:
  - `Authorization: Bearer {jwt_token}`
- **Response**:
  - `204 No Content`: Task successfully deleted
  - `401 Unauthorized`: Invalid or missing authentication
  - `403 Forbidden`: User attempting to delete another user's task
  - `404 Not Found`: Task or user ID does not exist
- **Response Body**: Empty

### PATCH /api/{user_id}/tasks/{id}/complete
- **Description**: Toggle the completion status of a task for the specified user
- **Method**: PATCH
- **Authentication**: Required (valid JWT token)
- **Path Parameters**:
  - `{user_id}`: User identifier (must match authenticated user)
  - `{id}`: Task identifier
- **Request Headers**:
  - `Authorization: Bearer {jwt_token}`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "completed": true
  }
  ```
- **Response**:
  - `200 OK`: Task completion status successfully updated
  - `400 Bad Request`: Invalid request body or missing completed field
  - `401 Unauthorized`: Invalid or missing authentication
  - `403 Forbidden`: User attempting to update another user's task
  - `404 Not Found`: Task or user ID does not exist
- **Response Body**:
  ```json
  {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "title": "Task title",
    "description": "Optional task description",
    "completed": true,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z"
  }
  ```

## Authentication Requirements

All endpoints require valid JWT authentication via the `Authorization` header:
- Format: `Authorization: Bearer {jwt_token}`
- Token must be valid and not expired
- User ID in token must match the `{user_id}` in the path
- Invalid tokens result in 401 Unauthorized responses

## Error Responses and Status Codes

### Standard Error Response Format
```json
{
  "error": "Error message describing the issue",
  "code": "Error code identifier",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### HTTP Status Codes
- `200 OK`: Request successful with response body
- `201 Created`: Resource successfully created
- `204 No Content`: Request successful with no response body
- `400 Bad Request`: Invalid request parameters or body
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions for the request
- `404 Not Found`: Requested resource does not exist
- `405 Method Not Allowed`: HTTP method not supported for endpoint
- `422 Unprocessable Entity`: Semantic errors in request
- `500 Internal Server Error`: Unexpected server error

### Common Error Codes
- `INVALID_REQUEST`: Request body or parameters are invalid
- `AUTHENTICATION_FAILED`: Authentication token is invalid
- `INSUFFICIENT_PERMISSIONS`: User lacks required permissions
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `VALIDATION_ERROR`: Request validation failed
- `INTERNAL_ERROR`: Unexpected server error occurred