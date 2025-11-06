"""Flask web application for video recommendation system."""
import os
import json
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from dotenv import load_dotenv
from video_generator import generate_initial_videos, generate_video_pool, format_video_for_prompt
from recommender import VideoRecommender
from analytics import calculate_familiarity_score, get_preference_insights

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

# Load pre-generated thumbnails from config
THUMBNAILS_POOL = []
try:
    with open("thumbnails_config.json", "r") as f:
        THUMBNAILS_POOL = json.load(f)
    print(f"✓ Loaded {len(THUMBNAILS_POOL)} pre-generated thumbnails")
except FileNotFoundError:
    print("⚠ Warning: thumbnails_config.json not found. Run generate_thumbnails_config.py first.")
    THUMBNAILS_POOL = generate_video_pool(1000, user_history=None)

# Initialize recommender lazily
recommender = None

def get_recommender():
    """Get or create the recommender instance."""
    global recommender
    if recommender is None:
        recommender = VideoRecommender()
    return recommender


@app.route("/")
def index():
    """Initial landing page with 3 starter videos."""
    # Reset session
    session.clear()

    # Pick 3 random initial videos from the pool
    import random
    initial_videos = random.sample(THUMBNAILS_POOL, 3)

    # Store in session
    session["history"] = []
    session["round"] = 0
    session["total_rounds"] = 0
    session["used_video_ids"] = []  # Track used IDs

    return render_template("index.html", videos=initial_videos)


@app.route("/choose", methods=["POST"])
def choose():
    """Handle user's video choice."""
    video_id = request.form.get("video_id")

    if not video_id:
        return redirect(url_for("index"))

    # Get current state
    round_num = session.get("round", 0)
    history = session.get("history", [])
    used_ids = session.get("used_video_ids", [])
    current_recommendations = session.get("current_recommendations", [])

    # Find the chosen video from the pool
    chosen_video = next((v for v in THUMBNAILS_POOL if v["id"] == video_id), None)

    if not chosen_video:
        return redirect(url_for("index"))

    # Track if user chose a recommended video (not the initial choice)
    if round_num > 0 and video_id in current_recommendations:
        session["recommendation_hits"] = session.get("recommendation_hits", 0) + 1

    # Track used video ID
    if video_id not in used_ids:
        used_ids.append(video_id)
        session["used_video_ids"] = used_ids

    # Add to history
    history.append(chosen_video)
    session["history"] = history
    session["total_rounds"] = session.get("total_rounds", 0) + 1

    # Generate new round
    return redirect(url_for("new_round"))


@app.route("/round")
def new_round():
    """Get Claude to recommend 3 thumbnails from the pre-generated pool."""
    history = session.get("history", [])
    used_ids = session.get("used_video_ids", [])

    if not history:
        return redirect(url_for("index"))

    # Get available thumbnails (excluding used ones)
    thumbnail_pool = [v for v in THUMBNAILS_POOL if v["id"] not in used_ids]

    if len(thumbnail_pool) < 3:
        # Pool exhausted
        return redirect(url_for("results"))

    # Use smart category-based recommendations for speed
    import random
    from collections import Counter

    # Get user's preferred categories from history
    category_counts = Counter([v["category"] for v in history])
    preferred_category = category_counts.most_common(1)[0][0] if category_counts else None

    # Find videos matching preferred category (60%) and diverse (40%)
    if preferred_category:
        matching = [v for v in thumbnail_pool if v["category"] == preferred_category][:10]
        diverse = [v for v in thumbnail_pool if v["category"] != preferred_category][:10]
        candidates = matching + diverse
        recommended_videos_sample = random.sample(candidates, min(3, len(candidates)))
        analysis_text = f"Based on your {len(history)} choices, you seem to enjoy {preferred_category} content. I'm showing you more {preferred_category} videos with some variety."
    else:
        recommended_videos_sample = random.sample(thumbnail_pool, min(3, len(thumbnail_pool)))
        analysis_text = "Exploring your interests with a diverse selection."

    recommended_ids = [v["id"] for v in recommended_videos_sample]

    # Calculate familiarity score
    familiarity_score = calculate_familiarity_score(history)

    # Get preference insights
    insights = get_preference_insights(history)

    session["current_recommendations"] = recommended_ids
    session["round"] = session.get("round", 0) + 1

    # Get the recommended video objects
    recommended_videos = [
        v for v in thumbnail_pool if v["id"] in recommended_ids
    ]

    # Debug logging
    print(f"[DEBUG] Round {session['round']}")
    print(f"[DEBUG] Analysis: {analysis_text}")
    print(f"[DEBUG] Familiarity Score: {familiarity_score}")
    print(f"[DEBUG] Insights: {insights}")

    return render_template(
        "round.html",
        videos=recommended_videos,
        round_num=session["round"],
        total_rounds=session["total_rounds"],
        pool_remaining=len(THUMBNAILS_POOL) - len(used_ids),
        analysis=analysis_text,
        familiarity_score=familiarity_score,
        insights=insights
    )


@app.route("/results")
def results():
    """Show results and statistics."""
    history = session.get("history", [])
    total_rounds = session.get("total_rounds", 0)
    recommendation_hits = session.get("recommendation_hits", 0)

    # Calculate statistics
    if not history:
        return redirect(url_for("index"))

    # Category distribution
    category_counts = {}
    for video in history:
        cat = video["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    # Recommendation accuracy (after initial choice)
    accuracy = 0
    if total_rounds > 1:
        accuracy = round((recommendation_hits / (total_rounds - 1)) * 100, 1)

    return render_template(
        "results.html",
        history=history,
        total_rounds=total_rounds,
        category_counts=category_counts,
        accuracy=accuracy,
        recommendation_hits=recommendation_hits
    )


@app.route("/funnel")
def funnel():
    """Visualization of recommendation funnel showing AI learning progression."""
    from collections import Counter

    history = session.get("history", [])

    if not history:
        return redirect(url_for("index"))

    # Category colors for visualization
    CATEGORY_COLORS = {
        "food": "#ef4444",
        "travel": "#3b82f6",
        "tech": "#8b5cf6",
        "lifestyle": "#ec4899",
        "education": "#10b981",
        "entertainment": "#f59e0b"
    }

    # Calculate initial distribution (all 1000 thumbnails)
    initial_counts = Counter([v["category"] for v in THUMBNAILS_POOL])
    initial_distribution = {}
    for category, count in initial_counts.items():
        initial_distribution[category] = {
            "count": count,
            "percentage": round((count / len(THUMBNAILS_POOL)) * 100, 1),
            "color": CATEGORY_COLORS.get(category, "#6b7280")
        }

    # Build funnel levels for each choice
    funnel_levels = []
    cumulative_used_ids = []

    for i, chosen_video in enumerate(history):
        # Track used IDs up to this point
        cumulative_used_ids.append(chosen_video["id"])

        # Get remaining pool after this choice
        remaining_pool = [v for v in THUMBNAILS_POOL if v["id"] not in cumulative_used_ids]

        # Calculate category distribution in remaining pool
        remaining_counts = Counter([v["category"] for v in remaining_pool])
        distribution = {}
        for category, count in remaining_counts.items():
            distribution[category] = {
                "count": count,
                "percentage": round((count / len(remaining_pool)) * 100, 1) if remaining_pool else 0,
                "color": CATEGORY_COLORS.get(category, "#6b7280")
            }

        # Calculate user's preferred category so far
        history_so_far = history[:i+1]
        category_preference = Counter([v["category"] for v in history_so_far])
        preferred_category = category_preference.most_common(1)[0][0] if category_preference else None

        # Generate insight about AI learning
        if i == 0:
            insight = f"First choice revealed interest in {chosen_video['category']} content. Filtering begins."
        else:
            if chosen_video["category"] == preferred_category:
                insight = f"Confirmed preference for {preferred_category}. Narrowing focus on similar content."
            else:
                insight = f"Exploring {chosen_video['category']} while maintaining {preferred_category} as primary interest."

        # Calculate familiarity score at this point
        familiarity_score = calculate_familiarity_score(history_so_far)

        funnel_levels.append({
            "chosen": chosen_video,
            "remaining": len(remaining_pool),
            "distribution": distribution,
            "preferred_category": preferred_category,
            "insight": insight,
            "familiarity_score": familiarity_score
        })

    # Final stats
    final_category_counts = Counter([v["category"] for v in history])
    primary_category = final_category_counts.most_common(1)[0][0] if final_category_counts else "None"

    final_stats = {
        "primary_category": primary_category,
        "familiarity": calculate_familiarity_score(history),
        "remaining": len([v for v in THUMBNAILS_POOL if v["id"] not in cumulative_used_ids])
    }

    return render_template(
        "funnel.html",
        initial_distribution=initial_distribution,
        funnel_levels=funnel_levels,
        final_stats=final_stats
    )


@app.route("/continue", methods=["POST"])
def continue_session():
    """Continue to next round."""
    return redirect(url_for("new_round"))


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    """API endpoint for infinite scroll - get recommendations after a choice."""
    data = request.get_json()
    video_id = data.get("video_id")

    if not video_id:
        return jsonify({"error": "No video_id provided"}), 400

    history = session.get("history", [])
    used_ids = session.get("used_video_ids", [])
    previous_recommendations = session.get("current_recommendations", [])

    # Find the chosen video from the pool
    chosen_video = next((v for v in THUMBNAILS_POOL if v["id"] == video_id), None)

    if not chosen_video:
        return jsonify({"error": "Video not found"}), 404

    # Track if user chose a recommended video (not the initial 3)
    if previous_recommendations and video_id in previous_recommendations:
        session["recommendation_hits"] = session.get("recommendation_hits", 0) + 1

    # Add to history
    history.append(chosen_video)
    session["history"] = history
    session["total_rounds"] = session.get("total_rounds", 0) + 1

    # Track used video
    if video_id not in used_ids:
        used_ids.append(video_id)
        session["used_video_ids"] = used_ids

    # Get available thumbnails (excluding used ones)
    available_pool = [v for v in THUMBNAILS_POOL if v["id"] not in used_ids]

    if len(available_pool) < 3:
        return jsonify({
            "error": "Pool exhausted",
            "message": "You've explored all available thumbnails!"
        }), 200

    # Get recommendations from Claude
    history_for_prompt = [format_video_for_prompt(v) for v in history]
    candidates_for_prompt = [format_video_for_prompt(v) for v in available_pool[:100]]  # Limit to 100 for performance

    analysis_text = "Analyzing your preferences..."
    recommended_videos = []

    try:
        rec = get_recommender()
        recommended_ids, analysis_text = rec.recommend(history_for_prompt, candidates_for_prompt, 3)

        # Get the recommended video objects
        recommended_videos = [v for v in available_pool if v["id"] in recommended_ids]

        # Track these as used
        for rec_id in recommended_ids:
            if rec_id not in used_ids:
                used_ids.append(rec_id)
        session["used_video_ids"] = used_ids

    except Exception as e:
        print(f"Recommendation error: {e}")
        import traceback
        traceback.print_exc()
        # Fallback to random
        import random
        recommended_videos = random.sample(available_pool, min(3, len(available_pool)))
        analysis_text = "Unable to analyze preferences at this time. Showing random selections."

    # Calculate familiarity score and insights
    familiarity_score = calculate_familiarity_score(history)
    insights = get_preference_insights(history)

    session["round"] = session.get("round", 0) + 1

    # Store current recommendations for next click tracking
    session["current_recommendations"] = [v["id"] for v in recommended_videos]

    return jsonify({
        "success": True,
        "recommendations": recommended_videos,
        "analysis": analysis_text,
        "familiarity_score": familiarity_score,
        "insights": insights,
        "round": session["round"],
        "total_rounds": session["total_rounds"],
        "pool_remaining": len(available_pool) - 3
    })


@app.route("/api/stats")
def api_stats():
    """API endpoint for current statistics."""
    history = session.get("history", [])
    total_rounds = session.get("total_rounds", 0)

    category_counts = {}
    for video in history:
        cat = video["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

    return jsonify({
        "total_rounds": total_rounds,
        "categories": category_counts,
        "history_count": len(history)
    })


@app.route("/test/analytics")
def test_analytics():
    """Test endpoint to verify analytics are working."""
    from video_generator import generate_thumbnail

    # Create test history
    test_history = [
        generate_thumbnail(category='food'),
        generate_thumbnail(category='food'),
    ]

    familiarity_score = calculate_familiarity_score(test_history)
    insights = get_preference_insights(test_history)

    return jsonify({
        "familiarity_score": familiarity_score,
        "insights": insights,
        "test_history": [{"title": v["title"], "category": v["category"]} for v in test_history],
        "message": "Analytics working! Familiarity score and insights generated successfully."
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 6006))
    app.run(host="0.0.0.0", port=port, debug=True)
