FROM python:3.13-slim
LABEL authors="mskar"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY=dummy-build-time-key
ENV DB_PASSWORD=dummy-build-time-password
ENV DB_HOST=localhost
ENV DB_USER=postgres
ENV DB_NAME=vulntrack
ENV SECRET_KEY=dummy-build-time-key
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "VulnTrackAdmin.wsgi:application", "--bind", "0.0.0.0:8000"]

