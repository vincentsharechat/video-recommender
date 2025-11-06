"""Generate realistic thumbnail-style content for recommendation testing."""
import random
import string


# Realistic thumbnail templates (typical clickbait/list-style content)
THUMBNAIL_TEMPLATES = {
    "food": {
        "locations": ["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune", "Kolkata", "Goa"],
        "templates": [
            "5 places to eat {food_type} in {location}",
            "Top 10 {food_type} spots in {location}",
            "Best {food_type} in {location} you MUST try",
            "{number} hidden {food_type} gems in {location}",
            "Cheap {food_type} places in {location}",
            "Ultimate {food_type} guide - {location}",
            "Street {food_type} tour in {location}"
        ],
        "food_types": ["biryani", "dosa", "street food", "cafes", "restaurants", "breakfast", "dinner", "lunch", "desserts", "pizza", "burger", "chinese"],
        "tags": ["food", "foodie", "foodreview", "restaurants", "eating"]
    },
    "travel": {
        "locations": ["Bangalore", "Mumbai", "Delhi", "Goa", "Kerala", "Rajasthan", "Manali", "Ladakh", "Shimla", "Ooty"],
        "templates": [
            "{number} things to do in {location}",
            "Top {number} places to visit in {location}",
            "{location} travel guide 2024",
            "Hidden gems in {location}",
            "Budget trip to {location}",
            "48 hours in {location}",
            "{number} must-visit spots in {location}"
        ],
        "tags": ["travel", "travelguide", "tourism", "vacation", "explore"]
    },
    "tech": {
        "products": ["iPhone", "Android", "Laptop", "Gaming PC", "Tablet", "Smartwatch", "Headphones", "Camera"],
        "templates": [
            "{product} review - worth it in 2024?",
            "Top {number} {product} under {price}",
            "{product} vs {product2} - which is better?",
            "Best {product} for {use_case}",
            "{product} unboxing and first impressions",
            "Don't buy {product} before watching this",
            "{number} {product} features you didn't know"
        ],
        "prices": ["10k", "20k", "30k", "50k", "1 lakh"],
        "use_cases": ["students", "professionals", "gamers", "creators", "beginners"],
        "tags": ["tech", "review", "gadgets", "technology", "unboxing"]
    },
    "lifestyle": {
        "topics": ["productivity", "morning routine", "fitness", "skincare", "fashion", "organization"],
        "templates": [
            "{number} ways to improve your {topic}",
            "My {topic} routine that changed my life",
            "{topic} tips for beginners",
            "How I {achievement} in {timeframe}",
            "{topic} mistakes you're making",
            "Budget {topic} guide",
            "{number} {topic} hacks you need to try"
        ],
        "achievements": ["lost 10kg", "became organized", "saved money", "got fit", "improved health"],
        "timeframes": ["30 days", "3 months", "6 months", "1 year"],
        "tags": ["lifestyle", "selfimprovement", "motivation", "tips", "hacks"]
    },
    "education": {
        "subjects": ["Python", "Web Development", "Data Science", "English", "Finance", "Marketing", "Photography", "Cooking"],
        "templates": [
            "Learn {subject} in {timeframe}",
            "{subject} crash course for beginners",
            "{number} {subject} tips everyone should know",
            "How to master {subject}",
            "{subject} tutorial - complete guide",
            "{subject} mistakes to avoid",
            "Free {subject} resources"
        ],
        "timeframes": ["10 minutes", "1 hour", "1 day", "1 week", "30 days"],
        "tags": ["education", "learning", "tutorial", "course", "howto"]
    },
    "entertainment": {
        "content_types": ["movies", "web series", "anime", "songs", "memes", "shorts", "vlogs"],
        "templates": [
            "Top {number} {content_type} to watch",
            "Best {content_type} of 2024",
            "{content_type} recommendations",
            "{number} underrated {content_type}",
            "Must-watch {content_type}",
            "Best {content_type} on {platform}",
            "{content_type} you missed"
        ],
        "platforms": ["Netflix", "Prime Video", "YouTube", "Hotstar", "Disney+"],
        "tags": ["entertainment", "recommendations", "mustwatch", "trending", "viral"]
    }
}

COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
    "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B739", "#52BE80",
    "#FF6347", "#20B2AA", "#778899", "#FF69B4", "#DDA0DD"
]


def generate_video_id():
    """Generate a unique video ID."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


def generate_thumbnail(category=None, video_id=None, context=None):
    """
    Generate a realistic thumbnail-style content.

    Args:
        category: Category to generate from (food, travel, tech, etc.)
        video_id: Optional video ID
        context: Optional context from previous choices to make related content
    """
    if video_id is None:
        video_id = generate_video_id()

    if category is None:
        category = random.choice(list(THUMBNAIL_TEMPLATES.keys()))

    template_data = THUMBNAIL_TEMPLATES[category]
    template = random.choice(template_data["templates"])

    # Generate title based on category
    if category == "food":
        location = random.choice(template_data["locations"])
        food_type = random.choice(template_data["food_types"])
        number = random.choice([3, 5, 7, 10])
        title = template.format(location=location, food_type=food_type, number=number)
        tags = [category, food_type, location.lower()] + random.sample(template_data["tags"], 2)

    elif category == "travel":
        location = random.choice(template_data["locations"])
        number = random.choice([3, 5, 7, 10])
        title = template.format(location=location, number=number)
        tags = [category, location.lower(), "travel"] + random.sample(template_data["tags"], 2)

    elif category == "tech":
        product = random.choice(template_data["products"])
        product2 = random.choice([p for p in template_data["products"] if p != product])
        number = random.choice([3, 5, 7, 10])
        price = random.choice(template_data["prices"])
        use_case = random.choice(template_data["use_cases"])
        title = template.format(
            product=product,
            product2=product2,
            number=number,
            price=price,
            use_case=use_case
        )
        tags = [category, product.lower(), "review"] + random.sample(template_data["tags"], 2)

    elif category == "lifestyle":
        topic = random.choice(template_data["topics"])
        number = random.choice([3, 5, 7, 10])
        achievement = random.choice(template_data["achievements"])
        timeframe = random.choice(template_data["timeframes"])
        title = template.format(
            topic=topic,
            number=number,
            achievement=achievement,
            timeframe=timeframe
        )
        tags = [category, topic, "tips"] + random.sample(template_data["tags"], 2)

    elif category == "education":
        subject = random.choice(template_data["subjects"])
        number = random.choice([3, 5, 7, 10])
        timeframe = random.choice(template_data["timeframes"])
        title = template.format(subject=subject, number=number, timeframe=timeframe)
        tags = [category, subject.lower(), "learning"] + random.sample(template_data["tags"], 2)

    elif category == "entertainment":
        content_type = random.choice(template_data["content_types"])
        number = random.choice([3, 5, 7, 10])
        platform = random.choice(template_data["platforms"])
        title = template.format(content_type=content_type, number=number, platform=platform)
        tags = [category, content_type, "recommendations"] + random.sample(template_data["tags"], 2)

    return {
        "id": video_id,
        "title": title,
        "category": category,
        "tags": tags[:5],  # Limit tags
        "duration": random.randint(5, 20),  # minutes
        "views": random.randint(10000, 5000000),
        "likes": random.randint(500, 200000),
        "thumbnail_color": random.choice(COLORS),
        "creator": f"Creator_{random.randint(1, 500)}"
    }


def generate_initial_videos():
    """Generate the initial 3 diverse videos for user to choose from."""
    categories = random.sample(list(THUMBNAIL_TEMPLATES.keys()), 3)
    return [
        generate_thumbnail(category=categories[0], video_id="vid001"),
        generate_thumbnail(category=categories[1], video_id="vid002"),
        generate_thumbnail(category=categories[2], video_id="vid003")
    ]


def generate_video_pool(count=50, user_history=None):
    """
    Generate a pool of videos with some contextual relevance to user history.

    Args:
        count: Number of videos to generate
        user_history: List of previously chosen videos

    Returns:
        List of video thumbnails
    """
    videos = []

    # If we have history, make 30% of videos related to user's preferences
    if user_history and len(user_history) > 0:
        # Analyze user preferences
        category_counts = {}
        all_tags = []

        for video in user_history:
            cat = video.get("category", "")
            category_counts[cat] = category_counts.get(cat, 0) + 1
            all_tags.extend(video.get("tags", []))

        # Get favorite category
        favorite_category = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else None

        # Generate 30% related content
        related_count = int(count * 0.3)
        if favorite_category and favorite_category in THUMBNAIL_TEMPLATES:
            for _ in range(related_count):
                videos.append(generate_thumbnail(category=favorite_category))

        # Generate 20% from other categories user has shown interest in
        for cat, cnt in category_counts.items():
            if cat != favorite_category and cat in THUMBNAIL_TEMPLATES:
                num_videos = min(int(count * 0.2), 10)
                for _ in range(num_videos):
                    videos.append(generate_thumbnail(category=cat))

    # Fill remaining with random diverse content
    remaining = count - len(videos)
    for _ in range(remaining):
        videos.append(generate_thumbnail())

    # Shuffle and return exact count
    random.shuffle(videos)
    return videos[:count]


def format_video_for_prompt(video):
    """Format video metadata for Claude prompt."""
    return {
        "id": video["id"],
        "title": video["title"],
        "category": video["category"],
        "tags": video["tags"][:3]
    }
