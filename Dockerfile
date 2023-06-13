# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy required files
COPY bible_bot.py /app/
COPY requirements.txt /app/

COPY .env.example /app/.env

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the bot
CMD ["python", "bible_bot.py"]