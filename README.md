# Talentadore

Talentadore is a microservices-based platform built with FastAPI, PostgreSQL, and Docker. The project follows a modular architecture with separate services for different functionalities.

## Project Structure

Below is the high-level architecture diagram of the Talentadore platform:

![Architecture Diagram](architecture.png)

The project is organized into several microservices and shared components:

```
talentadore/
├── shared/                  # Common code and utilities (git submodule)
├── member-service/          # Member management service (git submodule)
├── comment-service/         # Comment/feedback service (git submodule)
├── gateway-service/         # API Gateway service
├── docker-compose.yml       # Docker Compose configuration
└── .gitmodules             # Git submodule definitions
```

### Git Submodules

The project uses git submodules to manage shared code and individual services:

- `shared`: Common utilities, database models, and shared code
  - Repository: [ta-common](https://github.com/naseer617/ta-common)
- `member-service`: Handles member management and profiles
  - Repository: [ta-member-service](https://github.com/naseer617/ta-member-service)
- `comment-service`: Manages comments and feedback
  - Repository: [ta-comment-service](https://github.com/naseer617/ta-comment-service)

To clone the repository with submodules:
```bash
git clone --recursive git@github.com:naseer617/talentadore.git
cd talentadore
```

If you've already cloned the repository, initialize submodules with:
```bash
git submodule update --init --recursive
```

## Docker Setup

The project uses Docker Compose to manage multiple services and their dependencies. The setup includes:

### Services

1. **Database Services**
   - `comment-db`: PostgreSQL database for the comment service
     - Port: 5433
     - Database: comment_db
   - `member-db`: PostgreSQL database for the member service
     - Port: 5434
     - Database: member_db

2. **Application Services**
   - `comment-service`: Handles comments and feedback
   - `member-service`: Manages member profiles
   - `gateway-service`: API Gateway (port 8000)

### Environment Variables

Create a `.env` file in the root directory with the following variables:
```env
# Database Credentials
COMMENT_DB_USER=your_comment_db_user
COMMENT_DB_PASSWORD=your_comment_db_password
MEMBER_DB_USER=your_member_db_user
MEMBER_DB_PASSWORD=your_member_db_password
```

### Running the Services

1. Build and start all services:
```bash
docker compose up --build
```

2. Start services in detached mode:
```bash
docker compose up -d
```

3. View logs:
```bash
docker compose logs -f
```

4. Stop all services:
```bash
docker compose down
```

### API Documentation

Once the services are running, you can access the API documentation through the following URLs:

- **Gateway Service API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
  - Interactive Swagger UI documentation
  - Test API endpoints directly from the browser
  - View request/response schemas and models

## API Testing with curl

You can test the API endpoints using curl commands. Here are examples for both services:

### Member Service

1. Create a member:
```bash
curl -X POST http://localhost:8000/members \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "login": "johndoe",
    "email": "john.doe@example.com",
    "title": "Software Engineer",
    "avatar_url": "https://example.com/avatar.jpg",
    "followers": 0,
    "following": 0
  }'
```

2. Get all members:
```bash
curl -X GET http://localhost:8000/members
```

3. Delete all members (soft delete):
```bash
curl -X DELETE http://localhost:8000/members
```

4. Delete a specific member (replace {id} with actual member ID):
```bash
curl -X DELETE http://localhost:8000/members/{id}
```

### Comment Service

1. Create a comment:
```bash
curl -X POST http://localhost:8000/comments \
  -H "Content-Type: application/json" \
  -d '{"feedback": "This is a test comment"}'
```

2. Get all comments:
```bash
curl -X GET http://localhost:8000/comments
```

3. Delete all comments (soft delete):
```bash
curl -X DELETE http://localhost:8000/comments
```

4. Delete a specific comment (replace {id} with actual comment ID):
```bash
curl -X DELETE http://localhost:8000/comments/{id}
```

### Complete Test Flow

Here's a complete test flow that creates and deletes both a member and a comment:

```bash
# 1. Create a member
curl -X POST http://localhost:8000/members \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "login": "johndoe",
    "email": "john.doe@example.com",
    "title": "Software Engineer"
  }'

# 2. Create a comment
curl -X POST http://localhost:8000/comments \
  -H "Content-Type: application/json" \
  -d '{"feedback": "Great service!"}'

# 3. Get all members and comments to see IDs
curl -X GET http://localhost:8000/members
curl -X GET http://localhost:8000/comments

# 4. Delete specific member and comment (replace {member_id} and {comment_id} with actual IDs)
curl -X DELETE http://localhost:8000/members/{member_id}
curl -X DELETE http://localhost:8000/comments/{comment_id}
```

Note:
- All endpoints return JSON responses
- POST requests require the `Content-Type: application/json` header
- Member creation requires at least `first_name`, `last_name`, `login`, and `email` fields
- Comment creation only requires the `feedback` field
- DELETE endpoints perform soft deletes (they mark records as deleted but don't remove them from the database)

## Testing

Each service includes its own test suite with setup scripts and test runners. The test environment requires a virtual environment and a test database.

### Test Setup

1. **Setup Script (`setup-test-env.sh`)**
   - Creates a Python virtual environment (`.venv`)
   - Installs test dependencies from `requirements-test.txt`
   - Sets up a test database using Docker Compose
   - Creates necessary test configuration files
   - Sets up environment variables for testing

   To run the setup script:
   ```bash
   cd <service-directory>  # e.g., comment-service or member-service
   chmod +x tests/setup-test.sh
   ./tests/setup-tests.sh
   ```

2. **Test Database**
   - Each service has its own test database configuration in `tests/test-config/docker-compose.test.yml`
   - The test database runs on a different port to avoid conflicts with development databases
   - Test data is isolated from development data

### Running Tests

Before running tests, ensure you're in the service directory and have activated the virtual environment:

```bash
cd <service-directory>  # e.g., comment-service or member-service
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
```

Then you can run either:

1. **Basic Tests** (`run-tests.sh`):
   ```bash
   ./tests/run-tests.sh
   ```
   This script:
   - Activates the virtual environment
   - Starts the test database
   - Runs pytest with basic configuration
   - Tears down the test database

2. **Tests with Coverage** (`run-coverage.sh`):
   ```bash
   ./tests/run-coverage.sh
   ```
   This script:
   - Activates the virtual environment
   - Starts the test database
   - Runs pytest with coverage reporting
   - Generates a coverage report
   - Tears down the test database

### Test Configuration

- Test configuration is in `tests/test-config/pytest.ini`
- Environment variables for tests are in `tests/test-config/.env.test`
- Test database settings are in `tests/test-config/docker-compose.test.yml`

### Example Test Run

```bash
# For comment-service
cd comment-service
source .venv/bin/activate
./tests/run-tests.sh

# For member-service
cd member-service
source .venv/bin/activate
./tests/run-tests.sh

# To run with coverage
./tests/run-coverage.sh
```

Note: Always ensure you're in the virtual environment before running tests. The test scripts will check for this and warn you if you're not.
