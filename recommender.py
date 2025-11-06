"""Claude-powered video recommendation engine."""
import json
import os
from anthropic import Anthropic


class VideoRecommender:
    """Uses Claude API to recommend videos based on user history."""

    def __init__(self, api_key=None):
        """Initialize the recommender with API key."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.client = Anthropic(api_key=self.api_key)

    def recommend(self, user_history, candidate_videos, num_recommendations=3):
        """
        Recommend videos from candidates based on user history.

        Args:
            user_history: List of dicts with video metadata user has chosen
            candidate_videos: List of candidate videos to choose from
            num_recommendations: Number of recommendations to return (default: 3)

        Returns:
            Tuple: (recommended_ids, analysis_text)
        """
        prompt = self._build_prompt(user_history, candidate_videos, num_recommendations)

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Latest working Claude 3.5
                max_tokens=512,  # Reduced for speed
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the response text
            response_text = message.content[0].text

            # Try to extract JSON and analysis
            analysis_text = None
            recommended_ids = []

            # Look for JSON array in response
            import re
            json_match = re.search(r'\[[\s\S]*?\]', response_text)
            if json_match:
                recommended_ids = json.loads(json_match.group())
                # Everything before JSON is analysis
                analysis_text = response_text[:json_match.start()].strip()
                if not analysis_text:
                    # Everything after JSON might be analysis
                    analysis_text = response_text[json_match.end():].strip()

            # Validate recommendations
            candidate_ids = {v["id"] for v in candidate_videos}
            valid_recommendations = [
                vid_id for vid_id in recommended_ids
                if vid_id in candidate_ids
            ][:num_recommendations]

            # If we didn't get enough valid recommendations, fill with random candidates
            if len(valid_recommendations) < num_recommendations:
                remaining_candidates = [
                    v["id"] for v in candidate_videos
                    if v["id"] not in valid_recommendations
                ]
                import random
                additional = random.sample(
                    remaining_candidates,
                    num_recommendations - len(valid_recommendations)
                )
                valid_recommendations.extend(additional)

            return valid_recommendations, analysis_text

        except Exception as e:
            print(f"Error in Claude API call: {e}")
            # Fallback: return random videos
            import random
            return [v["id"] for v in random.sample(candidate_videos, num_recommendations)], None

    def _build_prompt(self, user_history, candidate_videos, num_recommendations):
        """Build the prompt for Claude API."""

        # Format user history
        if not user_history:
            history_text = "No previous choices yet (this is the first round)."
        else:
            history_items = []
            for i, video in enumerate(user_history, 1):
                history_items.append(
                    f"{i}. \"{video['title']}\" (Category: {video['category']}, Tags: {', '.join(video['tags'][:3])})"
                )
            history_text = "\n".join(history_items)

        # Format candidate videos
        candidate_items = []
        for video in candidate_videos:
            candidate_items.append(
                f"- ID: {video['id']} | Title: \"{video['title']}\" | "
                f"Category: {video['category']} | Tags: {', '.join(video['tags'][:3])}"
            )
        candidates_text = "\n".join(candidate_items)

        prompt = f"""You are an intelligent content recommendation engine analyzing user behavior. Your goal is to predict which thumbnails a user will most likely click based on their viewing history.

USER'S VIEWING HISTORY:
{history_text}

CANDIDATE THUMBNAILS (100 available):
{candidates_text}

TASK:
From these 100 pre-generated thumbnails, select the {num_recommendations} that are MOST RELEVANT to the user's interests. Look for CLEAR PATTERNS and CONTEXTUAL RELEVANCE to maximize engagement.

CRITICAL ANALYSIS POINTS:
1. **Location Patterns**: If user chose content about "Bangalore" or "Mumbai", prioritize other content from the same location
2. **Topic Continuity**: If user chose "food" content, they're likely interested in more food content (restaurants, cafes, recipes, etc.)
3. **Category Preferences**: If user picked "tech" or "travel", favor similar categories
4. **Specific Interests**: Extract specific topics from titles (e.g., "biryani", "iPhone review", "budget travel")
5. **Tag Overlap**: Match tags between history and candidates
6. **Logical Progression**: Pick content that naturally extends their interests (e.g., "5 places to eat in Bangalore" → "Best cafes in Bangalore" or "Street food in Bangalore")

EXAMPLES OF GOOD RECOMMENDATIONS:
- User picked "5 places to eat in Bangalore" → Recommend "Best cafes in Bangalore" or "Street food tour in Bangalore"
- User picked "iPhone review" → Recommend "Top 5 iPhone accessories" or "iPhone vs Android"
- User picked "Budget trip to Goa" → Recommend "Hidden gems in Goa" or "Things to do in Goa"

Choose content that feels like a natural, logical next step in their content journey.

RESPONSE FORMAT:
First, provide your analysis (2-3 sentences) about the user's interests and why you picked these recommendations.
Then, on a new line, provide ONLY the JSON array of {num_recommendations} video IDs.

Example:
The user shows strong interest in food content, particularly in Bangalore. I'm recommending related food spots in the same city and expanding to cafes and street food based on their previous restaurant choices.

["video_id_1", "video_id_2", "video_id_3"]"""

        return prompt
