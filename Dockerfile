FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

RUN pip3 install --upgrade pip
RUN pip3 install Django
RUN pip3 install djangorestframework
RUN pip3 install python-dotenv
RUN pip3 install django-cors-headers
RUN pip3 install requests
RUN pip3 install dataclasses-serialization
RUN pip3 install django-tailwind
RUN pip3 install 'django-tailwind[reload]'

EXPOSE 8000

CMD ["sh", "-c", "\
    python manage.py makemigrations api && \
    python manage.py migrate && \
    echo \"from django.contrib.auth import get_user_model; \
    User = get_user_model(); \
    User.objects.filter(username='admin').exists() or \
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python manage.py shell && \
    python manage.py runserver 0.0.0.0:8000"]