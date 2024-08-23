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

RUN pip3 manage.py makemigrations api
RUN pip3 manage.py migrate

EXPOSE 8000

# Run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
