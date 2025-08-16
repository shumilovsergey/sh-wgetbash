# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django web application that generates bash scripts for system automation. The platform allows users to create, manage, and combine bash scripts into templates that can be downloaded as executable files. It integrates with Telegram for user authentication and features a modern light angular CSS design.

## Architecture

### Core Applications
- **api**: Main application handling script and template management, user sessions, and web views
- **bot**: Telegram bot integration for user authentication
- **server**: Django project configuration and settings

### Key Models (api/models.py)
- `TelegramUsers`: User management linked to Telegram accounts
- `Scripts`: Individual bash scripts with authorship tracking
- `Templates`: Collections of scripts that can be combined into single bash files
- `MainPage`: CMS-like content for the homepage

### Authentication Flow
1. User visits site and gets session ID
2. Redirected to Telegram bot with session parameter
3. Bot authenticates user and links session to Telegram account
4. User gains access to script/template management features

### Script Generation
- Scripts are wrapped with bash headers and separators (defined in server/const.py)
- Templates combine multiple scripts into a single downloadable bash file
- Raw script downloads include proper bash shebang and completion messages
- Self-cleaning scripts: Downloaded scripts automatically delete themselves after execution

## Development Commands

### Django Development
```bash
# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (credentials: admin/admin)
python manage.py createsuperuser

# Django shell
python manage.py shell
```

### Frontend Development
The application uses custom CSS with a modern light angular design:
- Main stylesheet: `api/static/css/styles.css` - Modern light angular design with 8px grid system
- JavaScript enhancements: `api/static/js/app.js` - Interactive features
- No build process required - CSS and JS are served directly

### Quick Development Setup
```bash
# Manual setup for local development
python3 -m venv venv
source venv/bin/activate
pip install django python-dotenv djangorestframework django-cors-headers requests dataclasses-serialization markdown
python manage.py makemigrations api && python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Docker Development
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d
```

## Environment Configuration

Required environment variables (set in env.env):
- `TOKEN_TG`: Telegram bot token
- `HOST_DNS`: Domain name for the application
- `BOT_NAME`: Telegram bot username

## Database

- Uses SQLite3 by default (stored in sqlite/db.sqlite3)
- Automatic migrations run on Docker container startup
- Admin user automatically created with credentials admin/admin

## URL Structure

### Main Routes (api/urls.py)
- `/`: Homepage with main content
- `/login/`: Redirect to Telegram authentication
- `/logout/`: Clear session and logout
- `/auth_check/`: AJAX endpoint to verify authentication status

### Script Management
- `/script_create/`: Create new bash scripts
- `/script_list/`: List user's scripts
- `/script_id/<id>/`: View/edit specific script
- `/script_raw/<id>/`: Download script as .sh file

### Template Management
- `/template_create/`: Create script collections
- `/template_list/`: List user's templates
- `/template_id/<id>/`: View specific template
- `/template_raw/<id>/`: Download template as combined .sh file

## Security Notes

- Authentication is handled through Telegram OAuth
- Session-based access control for script/template operations
- Users can only modify their own scripts and templates
- CORS and CSRF protection configured for API endpoints

## Testing and Quality

The project does not include explicit test commands or linting configuration. When working on the codebase:
- Django tests can be run with `python manage.py test`
- Code quality should follow Django best practices
- No specific linting or formatting tools are configured

## Dependency Management

Python dependencies are installed via pip in the Dockerfile:
- Core: Django, DRF, CORS headers, dotenv, requests, dataclasses-serialization, markdown
- No requirements.txt file exists - dependencies are managed in Dockerfile
- For local development, dependencies must be installed manually in virtual environment

## Docker Configuration

The application is containerized with:
- Python 3.9 base image
- Auto-migration and superuser creation on startup (admin/admin)
- Exposed on port 8000 internally, mapped to 5008 externally via docker-compose
- Pre-built image available at ghcr.io/shumilovsergey/wgetbash:latest
- Local development server typically runs on port 8000

## Key Implementation Details

### Session Management and Authentication
- Custom middleware (`api.middleware`) handles session creation and debugging
- Session IDs are generated for anonymous users and linked to Telegram authentication
- Authentication flow requires Telegram bot interaction before accessing protected features

### Script Processing Pipeline
- Individual scripts are stored in the `Scripts` model with author tracking
- Templates combine multiple scripts using the `Templates` model with many-to-many relationships
- Script downloads include bash headers and separators defined in `server/const.py`
- Raw downloads format scripts with proper shebangs and completion messages

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.