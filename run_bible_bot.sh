#!/bin/bash

echo "Building Bible Bot Docker image..."
docker build -t biblebot .

echo "Running Bible Bot Docker container..."
docker run --name bible_bot_instance biblebot

echo "Cleaning up Bible Bot Docker container..."
docker rm bible_bot_instance
