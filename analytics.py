"""Analytics and user preference analysis."""


def calculate_familiarity_score(user_history):
    """
    Calculate how well we understand user preferences based on viewing history.

    Args:
        user_history: List of videos user has chosen

    Returns:
        int: Familiarity percentage (0-100)
    """
    if not user_history or len(user_history) == 0:
        return 0

    # Factors that increase familiarity
    num_videos = len(user_history)

    # 1. Basic familiarity from number of views (max 40%)
    # 1 video = 15%, 2 = 25%, 3 = 30%, 5 = 40%
    view_score = min(40, 15 + (num_videos - 1) * 5)

    # 2. Category consistency (max 30%)
    categories = [v.get("category", "") for v in user_history]
    category_counts = {}
    for cat in categories:
        category_counts[cat] = category_counts.get(cat, 0) + 1

    if len(category_counts) > 0:
        # Higher concentration in fewer categories = more familiar
        max_category_count = max(category_counts.values())
        category_ratio = max_category_count / len(user_history)
        category_score = int(category_ratio * 30)
    else:
        category_score = 0

    # 3. Tag/topic overlap (max 20%)
    all_tags = []
    for video in user_history:
        all_tags.extend(video.get("tags", []))

    tag_counts = {}
    for tag in all_tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1

    # Tags that appear multiple times indicate clear interests
    repeated_tags = sum(1 for count in tag_counts.values() if count >= 2)
    tag_score = min(20, repeated_tags * 5)

    # 4. Pattern strength (max 10%)
    # Check for location patterns, topic patterns, etc.
    pattern_score = 0

    # Check for location consistency in titles
    common_locations = ["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune", "Goa"]
    location_mentions = []
    for video in user_history:
        title = video.get("title", "")
        for loc in common_locations:
            if loc in title:
                location_mentions.append(loc)

    if len(location_mentions) >= 2:
        # User has location preference
        pattern_score += 5

    # Check for format patterns (Top N, Best X, etc.)
    format_patterns = ["Top", "Best", "places to", "things to", "How to"]
    format_matches = 0
    for video in user_history:
        title = video.get("title", "")
        if any(pattern in title for pattern in format_patterns):
            format_matches += 1

    if format_matches >= 2:
        pattern_score += 5

    # Total score
    total_score = min(100, view_score + category_score + tag_score + pattern_score)

    return total_score


def get_preference_insights(user_history):
    """
    Get insights about user preferences.

    Args:
        user_history: List of videos user has chosen

    Returns:
        dict: Insights about user preferences
    """
    if not user_history:
        return {
            "primary_interest": "Unknown",
            "secondary_interest": None,
            "patterns": []
        }

    # Category analysis
    categories = [v.get("category", "") for v in user_history]
    category_counts = {}
    for cat in categories:
        category_counts[cat] = category_counts.get(cat, 0) + 1

    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

    primary_interest = sorted_categories[0][0] if sorted_categories else "Unknown"
    secondary_interest = sorted_categories[1][0] if len(sorted_categories) > 1 else None

    # Detect patterns
    patterns = []

    # Location pattern
    common_locations = ["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune", "Goa"]
    location_counts = {}
    for video in user_history:
        title = video.get("title", "")
        for loc in common_locations:
            if loc in title:
                location_counts[loc] = location_counts.get(loc, 0) + 1

    if location_counts:
        top_location = max(location_counts.items(), key=lambda x: x[1])
        if top_location[1] >= 2:
            patterns.append(f"Focused on {top_location[0]} content")

    # Tag patterns
    all_tags = []
    for video in user_history:
        all_tags.extend(video.get("tags", []))

    tag_counts = {}
    for tag in all_tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1

    frequent_tags = [tag for tag, count in tag_counts.items() if count >= 2]
    if frequent_tags:
        patterns.append(f"Interest in: {', '.join(frequent_tags[:3])}")

    return {
        "primary_interest": primary_interest.capitalize(),
        "secondary_interest": secondary_interest.capitalize() if secondary_interest else None,
        "patterns": patterns
    }
