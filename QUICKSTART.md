# Quick Start Guide

## 🚀 Get Running in 3 Steps

### Step 1: Get Your API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key and copy it

### Step 2: Set Up Environment

```bash
cd video-recommender

# Copy the example env file
cp .env.example .env

# Edit .env and paste your API key
nano .env  # or use your favorite editor
```

Your `.env` should look like:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxx...
FLASK_SECRET_KEY=your_secret_key_here
```

### Step 3: Run the App

**Option A: Quick Start Script**
```bash
./start.sh
```

**Option B: Manual Start**
```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run the app
python app.py
```

**Option C: Docker**
```bash
docker-compose up
```

### Step 4: Open Browser

Navigate to: **http://localhost:5000**

## 🎮 How to Use

1. **Choose your first video** from 3 options
2. **Get AI recommendations** - Claude analyzes your choice and recommends 3 videos from 50 candidates
3. **Pick one** you'd engage with
4. **Repeat** - Watch how Claude learns your preferences
5. **View Results** - See statistics and AI accuracy

## 📊 Understanding Results

- **Total Videos Watched**: Number of videos you've chosen
- **AI Recommendation Hit Rate**: How often you picked Claude's recommendations
- **Category Preferences**: What types of content you gravitate toward
- **Viewing History**: Timeline of all your choices

## 🔧 Troubleshooting

**"ANTHROPIC_API_KEY not found"**
- Ensure `.env` file exists with valid API key
- Check no extra spaces in the key

**Port 5000 already in use**
- Stop other services on port 5000
- Or change port: `PORT=8000 python app.py`

**Module not found errors**
- Install dependencies: `pip install -r requirements.txt`

## 🎯 Tips for Testing

- Try choosing videos from different categories to see how Claude adapts
- The AI accuracy improves after 5-10 rounds as it learns your patterns
- Check the Results page to see category distribution and insights

## 📦 Deploy to Production

See the full [README.md](README.md) for deployment instructions to:
- Railway
- Render
- Fly.io
- Any Docker-compatible platform

Enjoy! 🎬
