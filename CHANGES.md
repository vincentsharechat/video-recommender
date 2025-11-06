# System Update: Pre-generated Thumbnail Pool

## Overview
Changed from generating 50 new videos per round to pre-generating 100 thumbnails at start and having Claude recommend the best 3.

## Key Changes

### 1. Pre-Generation at Start
**Before:** Generated 50 new videos each round
**After:** Generate 100 thumbnails once at session start

```python
# In index route
thumbnail_pool = generate_video_pool(100, user_history=None)
session["thumbnail_pool"] = thumbnail_pool
```

### 2. Claude Picks from Fixed Pool
**Before:** Claude chose from 50 newly generated videos
**After:** Claude analyzes all 100 pre-generated thumbnails and picks best 3

- More consistent recommendations
- Better pattern matching across the full pool
- Claude sees the complete landscape of content

### 3. Pool Management
- **Remove used thumbnails**: After user picks, thumbnail is removed from pool
- **Auto-regenerate**: When pool drops below 10 thumbnails, generate new 100
- **Contextual regeneration**: New pools are based on user history

### 4. UI Updates
- Shows remaining thumbnail count on each round
- Updated messaging to reflect pre-generation
- Shows pool size to user for transparency

## Benefits

### Performance
- ✅ Generate thumbnails once vs. every round
- ✅ Faster round transitions
- ✅ Less computation per recommendation

### Recommendation Quality
- ✅ Claude sees full pool of 100 options
- ✅ Better pattern matching and relevance
- ✅ More diverse recommendations available
- ✅ Can find best matches across larger set

### User Experience
- ✅ Instant recommendations (no waiting for generation)
- ✅ More consistent content quality
- ✅ Visibility into pool size
- ✅ Natural progression of content depletion

## Technical Implementation

### Session Data Structure
```python
{
    "thumbnail_pool": [100 videos],  # Pre-generated
    "history": [user_choices],
    "current_recommendations": [3 video_ids],
    "current_recommendations_videos": [3 video_objects],
    "round": int,
    "total_rounds": int,
    "recommendation_hits": int
}
```

### Flow
1. **Start**: Generate 3 initial + 100 pool thumbnails
2. **User picks**: Add to history, remove from pool
3. **Round N**: Claude picks best 3 from remaining pool
4. **Repeat**: Until pool < 10, then regenerate with context

### Auto-Regeneration Logic
```python
if len(thumbnail_pool) < 10:
    new_pool = generate_video_pool(100, user_history=history)
    session["thumbnail_pool"] = new_pool
```

## Files Modified

1. **app.py**
   - `index()`: Pre-generate 100 thumbnails
   - `choose()`: Remove picked thumbnail from pool
   - `new_round()`: Pick from existing pool instead of generating new

2. **recommender.py**
   - Updated prompt: "100 available" instead of "50 total"
   - Clarified task: "From these 100 pre-generated..."

3. **templates/index.html**
   - Added pre-generation messaging
   - Updated user instructions

4. **templates/round.html**
   - Show pool size in header
   - Display remaining thumbnails count

## Testing

```bash
cd ~/video-recommender
source venv/bin/activate
python test_setup.py
./start.sh
```

Open: http://localhost:6006

## Example Session

**Round 1:**
- Pool: 100 thumbnails
- User picks: "5 places to eat in Bangalore"
- Pool: 99 thumbnails

**Round 2:**
- Claude analyzes 99 thumbnails
- Recommends 3 most relevant to Bangalore food
- User picks: "Best cafes in Bangalore"
- Pool: 98 thumbnails

**Round 3:**
- Claude analyzes 98 thumbnails
- Continues logical progression
- ...

**Round 90+:**
- Pool drops below 10
- System auto-regenerates 100 new thumbnails based on user's viewing history
- Continues seamlessly

## Migration Notes

- No breaking changes to existing data
- Sessions reset on restart (by design)
- All existing functionality maintained
- Added backward compatibility checks
