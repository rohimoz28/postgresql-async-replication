# Gunakan Python 3.11 untuk kompatibilitas yang lebih baik
FROM python:3.11-alpine

# Set working directory di dalam container
WORKDIR /app

# Install dependency sistem yang dibutuhkan
RUN apk add --no-cache gcc musl-dev postgresql-dev curl

RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    python3-dev \
    musl-dev \
    linux-headers \
    build-base

# Copy file requirements dan install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy kode aplikasi
COPY ./app /app

# Expose port Flask
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Jalankan Flask
CMD ["python", "app.py"]