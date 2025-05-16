# Talentadore

Talentadore is a microservices-based platform built with FastAPI, PostgreSQL, and Docker. The project follows a modular architecture with separate services for different functionalities.

## Project Structure

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

### Development

Each service can be run independently for development:

1. **Comment Service**
```bash
cd comment-service
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. **Member Service**
```bash
cd member-service
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

3. **Gateway Service**
```bash
cd gateway-service
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

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
   chmod +x setup-test-env.sh
   ./setup-test-env.sh
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

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests to ensure everything works
4. Submit a pull request

## License

This project is licensed under the terms of the license included in the repository.
