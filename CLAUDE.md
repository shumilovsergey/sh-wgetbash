# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WgetBash is a Django-based web service for automating script execution on servers. The main concept is simplicity: generate a single command that can be pasted into a terminal to execute scripts remotely. The service provides a web interface for creating and managing bash scripts and templates.

## Architecture

This is a standard Django project with the following structure:

- **api/**: Django app handling web interface and API endpoints
  - Contains views, models, and templates for the main web application
  - Handles script creation, template management, and user sessions
  - Includes custom middleware for session management
- **bot/**: Django app for Telegram bot integration
  - Contains Telegram bot models and message handling logic
  - Manages Telegram users and bot interactions
- **server/**: Django project configuration
  - Settings, URLs, and WSGI/ASGI configuration
- **sqlite/**: Database directory for SQLite files
- **env/venv/**: Python virtual environments

## Database Models

Key models include:
- **TelegramUsers**: User authentication via Telegram
- **Scripts**: Individual bash scripts with name, author, and content
- **Templates**: Collections of scripts grouped together
- **MainPage**: Content management for the main page

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
source env/bin/activate
# or
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Django Management
```bash
# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

### Database Management
- Uses SQLite3 by default
- Database file located in `sqlite/db.sqlite3`
- Standard Django ORM operations apply

## Configuration

- Main settings in `server/settings.py`
- Environment variables loaded via python-dotenv from `.env` file
- CORS enabled for all origins (development setting)
- Debug mode enabled by default
- Telegram bot token configured via `TOKEN_TG` constant

## Key Dependencies

- Django 4.2+ with Django REST Framework
- python-dotenv for environment configuration
- django-cors-headers for CORS handling
- requests for HTTP operations
- dataclasses-serialization for data handling

## Docker Support

- `Dockerfile` and `docker-compose.yaml` present for containerized deployment
- Docker configuration suggests production deployment capability

## Security Notes

- Uses Django's built-in CSRF protection
- Session-based authentication with custom middleware
- Telegram integration for user authentication
- Default Django secret key present (should be changed for production)