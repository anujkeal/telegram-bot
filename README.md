# YouTube Downloader Telegram Bot

This bot allows you to send YouTube links via Telegram and get high-quality video (HD/4K) with audio merged.

## Features

- Downloads best video and audio separately
- Merges them into one MP4
- Sends it back via Telegram
- Uses `yt_dlp` + `ffmpeg`

## Requirements

- Python 3.10+
- ffmpeg installed and added to system PATH

## Running Locally

```bash
pip install -r requirements.txt
python video_bot.py
