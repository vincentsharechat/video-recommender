# Video Recommender with Claude AI

An intelligent content recommendation system that learns from user preferences using Claude AI. Features realistic, thumbnail-style content similar to YouTube/social media platforms.

## Features

- **Realistic Content**: Generates thumbnail-style content similar to YouTube (e.g., "5 places to eat in Bangalore", "Top 10 iPhone features")
- **Contextual Recommendations**: Claude AI makes logical recommendations based on your choices
  - Pick food content → Get more food recommendations
  - Pick Bangalore content → Get more Bangalore-related content
  - Pick tech reviews → Get more tech content
- **Smart Learning**: The more you engage, the better Claude understands your preferences
- **Results Dashboard**: Track viewing patterns, category preferences, and AI accuracy
- **6 Content Categories**: Food, Travel, Tech, Lifestyle, Education, Entertainment

## How It Works

1. User chooses one of 3 initial videos
2. System generates 50 random videos with diverse content
3. Claude AI analyzes user's viewing history and selects top 3 recommendations
4. User picks one video
5. Repeat - Claude keeps learning and improving recommendations
6. View statistics showing AI accuracy and viewing patterns

## Quick Start

### Prerequisites

- Python 3.11+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Option 1: Docker (Recommended)

```bash
# 1. Clone or navigate to the project directory
cd video-recommender

# 2. Create .env file with your API key
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env

# 3. Run with Docker Compose
docker-compose up

# 4. Open browser
open http://localhost:5000
```

### Option 2: Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Run the app
python app.py

# 5. Open browser
open http://localhost:5000
```

## Deployment

### Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add  # Add ANTHROPIC_API_KEY variable
railway up
```

### Deploy to Render

1. Connect your GitHub repository
2. Create a new Web Service
3. Set environment variable: `ANTHROPIC_API_KEY`
4. Deploy!

### Deploy to Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
flyctl launch
flyctl secrets set ANTHROPIC_API_KEY=your_key_here
flyctl deploy
```

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY` (required): Your Anthropic API key
- `FLASK_SECRET_KEY` (optional): Secret key for Flask sessions (auto-generated if not set)
- `PORT` (optional): Server port (default: 5000)

## Architecture

### Components

1. **video_generator.py**: Generates random videos with metadata (titles, categories, tags)
2. **recommender.py**: Claude AI integration for intelligent recommendations
3. **app.py**: Flask web application with session management
4. **templates/**: HTML templates with Tailwind CSS

### How Claude AI Works

Claude receives:
- User's viewing history (all previous choices)
- 50 candidate videos with metadata

Claude analyzes:
- Category preferences
- Topic patterns
- Tag overlap
- Content variety balance

Claude returns:
- Top 3 video IDs most likely to engage the user

## API Endpoints

- `GET /` - Initial video selection page
- `POST /choose` - Handle user video choice
- `GET /round` - Generate new round with AI recommendations
- `GET /results` - Display statistics and viewing history
- `POST /continue` - Continue to next round
- `GET /api/stats` - JSON API for current statistics

## Development

### Project Structure

```
video-recommender/
├── app.py                 # Flask application
├── recommender.py         # Claude API integration
├── video_generator.py     # Video generation
├── requirements.txt       # Dependencies
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
└── templates/
    ├── index.html        # Initial choice page
    ├── round.html        # Recommendation page
    └── results.html      # Statistics dashboard
```

### Customization

**Add more video categories**: Edit `CATEGORIES` in `video_generator.py`

**Change recommendation count**: Modify `num_recommendations` parameter in `app.py`

**Adjust Claude model**: Update `model` parameter in `recommender.py`

## License

MIT License - feel free to use and modify!

## Contributing

Contributions welcome! Please open an issue or submit a PR.

## Troubleshooting

**"ANTHROPIC_API_KEY not found"**
- Make sure you've created a `.env` file with your API key
- For Docker: ensure the environment variable is set in docker-compose.yml

**Claude API errors**
- Check your API key is valid
- Ensure you have sufficient API credits
- System will fallback to random recommendations if API fails

**Session issues**
- Sessions are stored in-memory (lost on restart)
- For production, consider using Redis for session storage

## Support

For issues or questions:
- Open an issue on GitHub
- Check Claude documentation: https://docs.anthropic.com
