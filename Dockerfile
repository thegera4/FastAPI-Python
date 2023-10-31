FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

# COPY all files from current directory to /app in container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 80
EXPOSE 80

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]