FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY bot_modernized.py .
COPY database.py .
COPY plants.py .
COPY localization.py .

# Create directory for data persistence
RUN mkdir -p /app/data

# Set environment variable for data file location
ENV DATA_FILE=/app/data/user_data.json

# Run the bot
CMD ["python3", "bot_modernized.py"]
