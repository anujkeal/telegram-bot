from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import yt_dlp
import os
import subprocess

TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("🔍 Downloading best video & audio...")

    # Output file names
    video_file = "temp_video.mp4"
    audio_file = "temp_audio.m4a"
    output_file = "final_video.mp4"

    # Delete old files if exist
    for f in [video_file, audio_file, output_file]:
        if os.path.exists(f):
            os.remove(f)

    try:
        # Step 1: Download best video (may be video-only)
        video_opts = {
            'format': 'bestvideo[ext=mp4]',
            'outtmpl': video_file,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([url])

        # Step 2: Download best audio (m4a = common for YouTube)
        audio_opts = {
            'format': 'bestaudio[ext=m4a]',
            'outtmpl': audio_file,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([url])

        # Step 3: Merge video + audio
        await update.message.reply_text("🔧 Merging video + audio...")

        cmd = [
            "ffmpeg", "-y",
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            output_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Step 4: Send file
        await update.message.reply_video(video=open(output_file, 'rb'), caption="✅ Done! High quality video with sound.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

    # Optional: Clean up files
    for f in [video_file, audio_file, output_file]:
        if os.path.exists(f):
            os.remove(f)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
