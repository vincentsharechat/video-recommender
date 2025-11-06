# New Features: AI Insights & Familiarity Tracking

## Overview
Added Claude's reasoning about user preferences and a dynamic familiarity percentage that grows as the system learns more about the user.

## What's New

### 1. Claude's Analysis 🤖
**Feature:** Claude now explains WHY it picked each recommendation

**What You See:**
- 2-3 sentence analysis of your interests
- Reasoning behind the recommendations
- Pattern recognition insights

**Example:**
> "The user shows strong interest in food content, particularly in Bangalore. I'm recommending related food spots in the same city and expanding to cafes and street food based on their previous restaurant choices."

### 2. Familiarity Score 📊
**Feature:** Dynamic percentage showing how well the system understands your preferences

**Score Breakdown:**
- **0-20%**: Just getting started
- **21-40%**: Seeing some patterns
- **41-60%**: Understanding your interests
- **61-80%**: Strong grasp of preferences
- **81-100%**: Expert-level understanding

**Factors That Increase Score:**
1. **Number of Videos Watched** (max 40%)
   - 1 video = 15%
   - 2 videos = 20%
   - 3 videos = 25%
   - 5+ videos = 40%

2. **Category Consistency** (max 30%)
   - Repeatedly choosing same category = higher score
   - Example: All food videos = 30%
   - Mixed categories = lower score

3. **Tag/Topic Overlap** (max 20%)
   - Tags appearing multiple times show clear interests
   - Example: "biryani", "bangalore" appearing 3+ times = 15%

4. **Pattern Strength** (max 10%)
   - Location patterns (e.g., always Bangalore content)
   - Format patterns (e.g., "Top N", "Best X")

### 3. Preference Insights 💡
**Feature:** Detailed breakdown of detected patterns

**Shows:**
- **Primary Interest**: Your main category (e.g., "Food")
- **Secondary Interest**: Second most common (e.g., "Travel")
- **Patterns Detected**:
  - Location focus (e.g., "Focused on Bangalore content")
  - Topic interests (e.g., "Interest in: biryani, cafes, street food")

### 4. Visual Display

#### Circular Progress Bar
```
     ┌─────┐
     │ 65% │  ← Your familiarity score
     │Familiar│
     └─────┘
  Understanding
   your taste
```

#### Analysis Card Layout
```
┌──────────────────────────────────────────────────────────┐
│ 🤖 Claude's Analysis                           65%       │
│                                             Familiar      │
│ The user shows strong interest in food content,          │
│ particularly in Bangalore. I'm recommending...           │
├──────────────────────────────────────────────────────────┤
│ Primary Interest  │ Secondary Interest │ Patterns        │
│ Food             │ Travel            │ • Bangalore     │
│                  │                   │ • food, cafes   │
└──────────────────────────────────────────────────────────┘
```

## Example User Journey

### Round 1
```
User picks: "5 places to eat in Bangalore"

Familiarity Score: 15%
Analysis: "Early preference detected for food content in Bangalore."
Primary Interest: Food
Patterns: None yet
```

### Round 2
```
User picks: "Best cafes in Bangalore"

Familiarity Score: 30%
Analysis: "User consistently chooses Bangalore food content.
Recommending more restaurants and cafes in the same location."
Primary Interest: Food
Patterns:
  • Focused on Bangalore content
```

### Round 3
```
User picks: "Street food tour in Bangalore"

Familiarity Score: 50%
Analysis: "Strong pattern: Bangalore food scene across different
formats (restaurants, cafes, street food). Diversifying within
this interest area."
Primary Interest: Food
Patterns:
  • Focused on Bangalore content
  • Interest in: food, restaurants, bangalore
```

### Round 5
```
Familiarity Score: 70%
Analysis: "Expert-level understanding of user's taste. They love
exploring Bangalore's diverse food scene from high-end restaurants
to street food. Recommending hidden gems and specific cuisines
they haven't explored yet."
Primary Interest: Food
Secondary Interest: Travel
Patterns:
  • Focused on Bangalore content
  • Interest in: food, restaurants, bangalore, cafes, street food
```

## Technical Implementation

### New Files
1. **analytics.py**
   - `calculate_familiarity_score(history)` - Calculates 0-100% score
   - `get_preference_insights(history)` - Extracts patterns

### Modified Files
1. **recommender.py**
   - Returns tuple: `(video_ids, analysis_text)`
   - Enhanced prompt to request analysis
   - Parses JSON + text response

2. **app.py**
   - Imports analytics functions
   - Calculates familiarity score each round
   - Passes insights to template

3. **templates/round.html**
   - New "AI Analysis & Insights" section
   - Circular progress bar for familiarity score
   - Preference breakdown display

## Benefits

### For Users
- ✅ **Transparency**: See why Claude picked recommendations
- ✅ **Trust**: Understand the AI's thought process
- ✅ **Progress**: Watch the system learn over time
- ✅ **Engagement**: Gamification through familiarity score

### For System
- ✅ **Explainability**: Claude's reasoning is visible
- ✅ **Feedback Loop**: Users can validate recommendations
- ✅ **Pattern Detection**: Clear visibility into learned preferences
- ✅ **Quality Assurance**: Catch poor recommendations early

## Testing

### Test the Analytics
```bash
cd ~/video-recommender
source venv/bin/activate
python -c "
from analytics import calculate_familiarity_score, get_preference_insights
from video_generator import generate_thumbnail

history = [
    generate_thumbnail(category='food'),
    generate_thumbnail(category='food'),
]

score = calculate_familiarity_score(history)
insights = get_preference_insights(history)

print(f'Score: {score}%')
print(f'Primary: {insights[\"primary_interest\"]}')
"
```

### Run the App
```bash
./start.sh
```

Open: http://localhost:6006

Watch the familiarity score grow with each choice!

## Future Enhancements

Possible additions:
- **Confidence Intervals**: Show certainty level for each recommendation
- **Preference Evolution**: Track how interests change over time
- **Diversity Score**: Balance between familiar and exploratory content
- **Mood Detection**: Analyze if user wants similar or different content
- **Time-based Patterns**: Morning vs evening content preferences
