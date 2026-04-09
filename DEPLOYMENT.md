# Deployment Guide

## Option 1: Render (Recommended - Free Tier Available)

Render is a modern cloud platform that offers free hosting for web applications.

### Steps:

1. Create a free account at [render.com](https://render.com)

2. Click "New +" and select "Web Service"

3. Connect your GitHub/GitLab repository or upload your code

4. Configure the service:
   - **Name**: natforms (or any name you want)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. Add Environment Variables:
   - `SECRET_KEY`: Generate a random string
   - `DATABASE_URL`: Leave empty (Render will provide SQLite)

6. Click "Create Web Service"

7. After deployment, run the database initialization:
   - Go to "Shell" tab in your Render dashboard
   - Run: `python init_db.py`

8. Your app will be available at: `https://natforms.onrender.com` (or your chosen name)

**Note**: Free tier apps on Render may take 30-60 seconds to wake up after inactivity.

### For Production Database (Optional):

If you need a persistent database:
1. Create a PostgreSQL database on Render (free tier available)
2. Copy the Internal Database URL
3. Set it as `DATABASE_URL` environment variable
4. Add `psycopg2-binary` to requirements.txt

---

## Option 2: Railway

Railway offers free hosting with a generous free tier.

### Steps:

1. Create account at [railway.app](https://railway.app)

2. Click "New Project" → "Deploy from GitHub repo"

3. Select your repository

4. Railway will auto-detect Python and deploy

5. Add Environment Variables in the project settings:
   - `SECRET_KEY`: Random string

6. Open the deployment URL

7. Run database initialization via Railway CLI or use the web shell

---

## Option 3: PythonAnywhere (Easy Setup)

PythonAnywhere is beginner-friendly with a free tier.

### Steps:

1. Create free account at [pythonanywhere.com](https://www.pythonanywhere.com)

2. Upload your code via:
   - Git clone from repository
   - Or upload files manually

3. Create a new web app:
   - Choose Flask
   - Python 3.10

4. Configure WSGI file to point to your app

5. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

6. Initialize database:
   ```bash
   python init_db.py
   ```

7. Reload your web app

---

## Option 4: Vercel (with limitations)

Vercel supports Python via serverless functions, but requires some modifications.

**Note**: Vercel is better for static sites and Node.js. For Python Flask apps, Render or Railway are better choices.

---

## Creating a QR Code

After deployment, create a QR code for your app:

1. Visit [qr-code-generator.com](https://www.qr-code-generator.com)
2. Enter your app URL (e.g., `https://natforms.onrender.com`)
3. Customize colors to match your brand (pink/purple tones)
4. Download as PNG or SVG
5. Print it large enough for the event (A4 or larger)

**Tip**: Test the QR code with multiple phones before the event!

---

## Pre-Event Checklist

- [ ] Deploy app and test all functionality
- [ ] Initialize database with your custom questions
- [ ] Test on mobile devices (iOS and Android)
- [ ] Generate and print QR code
- [ ] Test QR code with different phone cameras
- [ ] Ensure admin dashboard works
- [ ] Have backup plan (printed forms) if internet fails

---

## Custom Questions

To add your custom questions, edit the `init_db.py` file and replace the sample questions with your own. Then run:

```bash
python init_db.py
```

The format is:
```python
{
    "text": "Your question here?",
    "options": [
        {"text": "Option 1", "type": "romantic"},
        {"text": "Option 2", "type": "bold"},
        # ... more options
    ]
}
```

Available personality types:
- `romantic` - Romântica
- `bold` - Ousada
- `elegant` - Elegante
- `bohemian` - Boêmia
- `minimalist` - Minimalista
- `trendy` - Moderna
