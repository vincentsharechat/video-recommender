# Deployment Guide - Video Recommender

## Quick Deploy Options

### Option 1: Railway.app (Recommended - Easiest)
### Option 2: Render.com (Free Tier Available)
### Option 3: Fly.io (Docker-based)

---

## Step 1: Push to GitHub

### 1.1 Create GitHub Repository

```bash
cd ~/video-recommender

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Video Recommender with Claude AI

- Realistic thumbnail-style content generation
- Claude AI-powered recommendations with reasoning
- Pre-generated pool of 100 thumbnails
- Familiarity score tracking (0-100%)
- Preference insights and pattern detection
- Session management optimized for production
- Port 6006 configuration

Features:
- 6 content categories (food, travel, tech, lifestyle, education, entertainment)
- Contextual recommendations based on viewing history
- Visual analytics dashboard
- Docker support for easy deployment"

# Add your GitHub remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/video-recommender.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 1.2 Important: Don't Commit Secrets!

The `.gitignore` already excludes `.env`, but verify:

```bash
# Check .gitignore includes these:
cat .gitignore | grep -E "\.env|venv"

# If .env is tracked, remove it:
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
```

---

## Option 1: Railway.app Deployment

### Why Railway?
- ✅ Automatic deployments from GitHub
- ✅ Free tier: $5 credit/month
- ✅ Simple environment variable management
- ✅ Automatic HTTPS
- ✅ Built-in PostgreSQL/Redis if needed

### Steps:

1. **Sign up**: Go to [railway.app](https://railway.app) and sign up with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `video-recommender` repository
   - Railway will auto-detect it's a Python app

3. **Set Environment Variables**:
   - Go to your project → Variables tab
   - Add these variables:
     ```
     ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
     FLASK_SECRET_KEY=your-secret-key-here
     PORT=6006
     ```

4. **Configure Build**:
   Railway should auto-detect `requirements.txt`, but if needed:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`

5. **Deploy**:
   - Railway automatically deploys on every push to main
   - Get your URL from the deployment dashboard
   - Access at: `https://your-app.railway.app`

### Railway Configuration File (Optional)

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## Option 2: Render.com Deployment

### Why Render?
- ✅ Free tier available (sleeps after 15 min inactivity)
- ✅ GitHub integration
- ✅ Automatic SSL
- ✅ Easy to use

### Steps:

1. **Sign up**: Go to [render.com](https://render.com) and sign up with GitHub

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `video-recommender` repo

3. **Configure Service**:
   - **Name**: video-recommender
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app`
   - **Plan**: Free (or Starter for always-on)

4. **Environment Variables**:
   - Add in the "Environment" section:
     ```
     ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
     FLASK_SECRET_KEY=your-secret-key-here
     PYTHON_VERSION=3.11
     ```

5. **Deploy**:
   - Click "Create Web Service"
   - Render auto-deploys on every push to main
   - Access at: `https://video-recommender.onrender.com`

### Render Configuration File (Optional)

Create `render.yaml`:

```yaml
services:
  - type: web
    name: video-recommender
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: FLASK_SECRET_KEY
        generateValue: true
```

---

## Option 3: Fly.io Deployment (Docker)

### Why Fly.io?
- ✅ Docker-based (uses your Dockerfile)
- ✅ Free tier: 3 small VMs
- ✅ Global deployment
- ✅ Good performance

### Steps:

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**:
   ```bash
   flyctl auth login
   ```

3. **Initialize**:
   ```bash
   cd ~/video-recommender
   flyctl launch
   ```

   This creates `fly.toml`:
   ```toml
   app = "video-recommender"
   primary_region = "sjc"

   [build]
     dockerfile = "Dockerfile"

   [env]
     PORT = "6006"

   [[services]]
     internal_port = 6006
     protocol = "tcp"

     [[services.ports]]
       port = 80
       handlers = ["http"]

     [[services.ports]]
       port = 443
       handlers = ["tls", "http"]
   ```

4. **Set Secrets**:
   ```bash
   flyctl secrets set ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   flyctl secrets set FLASK_SECRET_KEY=your-secret-key-here
   ```

5. **Deploy**:
   ```bash
   flyctl deploy
   ```

6. **Open App**:
   ```bash
   flyctl open
   ```

---

## Automatic Deployments

### Railway & Render
- Automatically deploy on every push to `main`
- To deploy a specific branch, configure in settings

### Fly.io
Add GitHub Action `.github/workflows/fly-deploy.yml`:

```yaml
name: Fly Deploy
on:
  push:
    branches:
      - main

jobs:
  deploy:
    name: Deploy app
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

---

## Environment Variables Reference

All platforms need these:

| Variable | Description | Example |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Claude API key | `sk-ant-api03-...` |
| `FLASK_SECRET_KEY` | Flask session secret | Generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `PORT` | Server port (optional) | `6006` (Railway/Render set automatically) |

---

## Troubleshooting

### "Application Error" on load
- Check logs: `railway logs` or Render dashboard
- Verify environment variables are set
- Check Python version compatibility

### "Module not found"
- Ensure `requirements.txt` is in root directory
- Check build logs for pip install errors
- Try adding `--no-cache-dir` to pip install

### Session issues
- Verify `FLASK_SECRET_KEY` is set
- Check if cookies are being blocked
- Session size is optimized (< 4KB)

### Claude API errors
- Verify `ANTHROPIC_API_KEY` is correct
- Check API key has sufficient credits
- Model name is `claude-3-5-sonnet-20240620`

---

## Monitoring & Logs

### Railway
```bash
railway logs
```

### Render
- View logs in dashboard
- Or use Render CLI: `render logs video-recommender`

### Fly.io
```bash
flyctl logs
```

---

## Scaling

### Railway
- Auto-scales based on traffic
- Upgrade plan for more resources

### Render
- Free tier: 512MB RAM, 0.1 CPU
- Paid tier: More resources, always-on

### Fly.io
- Free: 3 shared-cpu-1x VMs
- Scale with: `flyctl scale count 3`

---

## Custom Domain

### Railway
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS records

### Render
1. Go to Settings → Custom Domain
2. Add domain and verify
3. SSL automatically provisioned

### Fly.io
```bash
flyctl certs add yourdomain.com
```

---

## Cost Estimates

### Railway
- Free: $5 credit/month (~500 hours)
- Hobby: $5/month (500 hours included)
- Pro: $20/month (usage-based)

### Render
- Free: Always available, sleeps after 15 min
- Starter: $7/month (always-on)
- Standard: $25/month (more resources)

### Fly.io
- Free: 3 VMs, 160GB transfer
- Paid: $1.94/VM/month + transfer costs

---

## Quick Deploy Checklist

- [ ] Push code to GitHub
- [ ] Choose platform (Railway/Render/Fly.io)
- [ ] Create account and connect GitHub
- [ ] Set environment variables
- [ ] Deploy!
- [ ] Test the live URL
- [ ] Set up custom domain (optional)
- [ ] Monitor logs for errors

---

## Need Help?

- Railway: https://docs.railway.app
- Render: https://render.com/docs
- Fly.io: https://fly.io/docs
- Flask: https://flask.palletsprojects.com/

Happy deploying! 🚀
