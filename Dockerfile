# ====================================================================
# Dockerfile - Antigravity Math Studio
# ====================================================================
FROM python:3.11-slim

# Thiết lập biến môi trường cơ bản
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8080 \
    SHOW_BROWSER=false

# Cài đặt các thư viện hệ thống cần thiết (font tiếng Việt, xử lý đồ họa, xml)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    fonts-dejavu-core \
    fonts-liberation \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Cài đặt thư viện Python trước để tận dụng Docker layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Tạo các thư mục làm việc mặc định
RUN mkdir -p input output/images output/history output/scripts

# Khai báo volume để dữ liệu đề thi và hình ảnh không bị mất khi restart container
VOLUME ["/app/input", "/app/output"]

# Mở cổng dịch vụ
EXPOSE 8080

# Chạy ứng dụng
CMD ["python", "app.py"]
