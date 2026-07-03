# Insta Creator Bot Setup
1. Upload all files to your GitHub repository.
2. Go to Render.com and create a New Web Service.
3. Link this repository.
4. Set Environment Variables:
   - `BOT_TOKEN` = Tumar Telegram bot token.
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn main:app`
