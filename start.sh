#!/bin/bash
# Install system tools
apt-get update && apt-get install -y yt-dlp ffmpeg

# Install Python libraries
pip install -r requirements.txt

# Jalankan aplikasi
exec python main.py
