# Funnel Visualization - How It Works

## Overview

The funnel visualization demonstrates how Claude AI progressively learns user preferences by showing an inverted pyramid that narrows from 1000 thumbnails down to increasingly personalized recommendations.

## Key Components

### 1. `/funnel` Route ([app.py:194-286](app.py#L194-L286))

**Purpose**: Backend endpoint that calculates funnel data for visualization

**How it works**:
```python
@app.route("/funnel")
def funnel():
    # 1. Get user's viewing history from session
    history = session.get("history", [])

    # 2. Calculate initial distribution across all 1000 thumbnails
    initial_counts = Counter([v["category"] for v in THUMBNAILS_POOL])

    # 3. Build funnel levels - one for each user choice
    for i, chosen_video in enumerate(history):
        # Track which videos have been used
        cumulative_used_ids.append(chosen_video["id"])

        # Calculate remaining pool after this choice
        remaining_pool = [v for v in THUMBNAILS_POOL if v["id"] not in cumulative_used_ids]

        # Calculate new category distribution
        remaining_counts = Counter([v["category"] for v in remaining_pool])

        # Determine user's preferred category so far
        preferred_category = category_preference.most_common(1)[0][0]

        # Generate AI learning insight
        if i == 0:
            insight = "First choice revealed interest in {category}. Filtering begins."
        else:
            insight = "Confirmed preference for {category}. Narrowing focus."

        # Calculate familiarity score progression
        familiarity_score = calculate_familiarity_score(history_so_far)
```

**Returns**:
- `initial_distribution`: Category breakdown of all 1000 thumbnails
- `funnel_levels`: Array of levels showing progression of AI learning
- `final_stats`: Primary category, familiarity %, and remaining videos

---

### 2. Funnel Template ([templates/funnel.html](templates/funnel.html))

**Purpose**: Renders the inverted pyramid visualization

**Structure**:

```html
<!-- Level 0: Initial Pool (1000 thumbnails) -->
<div class="funnel-layer" style="width: 100%;">
    <h3>Level 0: Initial Pool (1000 thumbnails)</h3>
    <!-- Category distribution bars -->
</div>

<!-- Level 1+: Each User Choice -->
{% for level in funnel_levels %}
<div class="funnel-layer" style="width: {{ 100 - (loop.index0 * 8) }}%;">
    <!-- Selected video with green border + pulse animation -->
    <div class="selected-marker">
        <!-- Video thumbnail and title -->
    </div>

    <!-- AI Learning Insight -->
    <div class="ai-insight">
        🤖 AI Learning: {{ level.insight }}
    </div>

    <!-- Category Distribution Bars -->
    <div class="category-bars">
        {% for category, data in level.distribution.items() %}
        <div class="bar" style="width: {{ data.percentage }}%; background: {{ data.color }};">
            {{ category }}: {{ data.count }} ({{ data.percentage }}%)
        </div>
        {% endfor %}
    </div>

    <!-- Familiarity Score Progress Bar -->
    <div class="familiarity-progress">
        Understanding: {{ level.familiarity_score }}%
    </div>
</div>
{% endfor %}
```

**Visual Features**:
- Each level narrows by 8% (`width: 100 - (loop.index * 8)%`)
- Selected videos have green border + pulse animation
- Color-coded category bars (food=red, tech=purple, travel=blue, etc.)
- Connector lines between levels
- Gradient progress bars for familiarity score

---

### 3. Navigation Integration

**Results Page** ([templates/results.html:88-93](templates/results.html#L88-L93)):
```html
<a href="/funnel" class="btn-purple">
    <svg><!-- Funnel icon --></svg>
    View Funnel Visualization
</a>
```

**Round Page** ([templates/round.html:149-154](templates/round.html#L149-L154)):
```html
<a href="/funnel" class="btn-purple">
    <svg><!-- Funnel icon --></svg>
    View Funnel
</a>
```

---

## Data Flow

```
User clicks video
    ↓
Session stores choice in history[]
    ↓
User navigates to /funnel
    ↓
Backend calculates:
  1. Initial 1000 thumbnail distribution
  2. For each choice:
     - Remaining pool (1000 - used_ids)
     - Category distribution changes
     - Preferred category
     - AI learning insight
     - Familiarity score
    ↓
Template renders:
  - Level 0 (full pool)
  - Level 1-N (progressively narrower)
  - Final stats
```

---

## Key Algorithms

### Category Distribution Calculation
```python
remaining_counts = Counter([v["category"] for v in remaining_pool])
for category, count in remaining_counts.items():
    percentage = round((count / len(remaining_pool)) * 100, 1)
```

### Preferred Category Tracking
```python
category_preference = Counter([v["category"] for v in history_so_far])
preferred_category = category_preference.most_common(1)[0][0]
```

### Familiarity Score
Uses `calculate_familiarity_score()` from [analytics.py](analytics.py):
- 0-100% score based on view count, category consistency, tag overlap
- Shows how well AI understands user preferences

---

## Visual Design

- **Colors**: Each category has a distinct color (defined in `CATEGORY_COLORS`)
- **Width**: Narrows progressively (100% → 92% → 84% → ...)
- **Animation**: Pulse effect on selected videos
- **Responsive**: Grid layout adapts to mobile/desktop

---

## Use Cases

1. **User**: Visualize how their choices influence recommendations
2. **Demo**: Show how AI learns preferences over time
3. **Debug**: Verify recommendation algorithm is working correctly
4. **Analytics**: Understand user behavior patterns

---

## Future Enhancements

- Add zoom/expand feature for each level
- Export funnel as image/PDF
- Compare multiple sessions side-by-side
- Show specific videos considered at each level (not just categories)
