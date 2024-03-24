FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
EXPOSE 3000
CMD ["python", "detection_backend/manage.py", "runserver", "0.0.0.0:8000"]
