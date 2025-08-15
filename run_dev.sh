#!/bin/bash

# WgetBash Development Server Script
echo "🚀 Starting WgetBash Development Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📥 Installing dependencies..."
    pip install django python-dotenv djangorestframework django-cors-headers requests
else
    echo "✅ Virtual environment found"
    source venv/bin/activate
fi

# Check if database exists and has data
if [ ! -f "sqlite/db.sqlite3" ]; then
    echo "🗄️  Setting up database..."
    python manage.py makemigrations
    python manage.py migrate
    echo "👤 Creating admin user (admin/admin)..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
fi

echo "🌐 Server will be available at:"
echo "   - Local: http://localhost:8990"
echo "   - Tunnel: https://wgetbash.sh-development.ru (update to port 8990)"
echo ""
echo "💡 Features:"
echo "   - Modern dark minimal design"
echo "   - No Tailwind CSS (custom CSS only)"
echo "   - Enhanced interactivity"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the server
python manage.py runserver 0.0.0.0:8990