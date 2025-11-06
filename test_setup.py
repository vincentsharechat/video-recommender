#!/usr/bin/env python
"""Test script to verify setup is correct."""
import sys

print("🧪 Testing Video Recommender Setup...\n")

# Test 1: Import modules
print("1. Testing module imports...")
try:
    import flask
    import anthropic
    from dotenv import load_dotenv
    import video_generator
    import recommender
    print("   ✅ All modules imported successfully")
except ImportError as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

# Test 2: Video generation
print("\n2. Testing video generation...")
try:
    from video_generator import generate_initial_videos, generate_video_pool
    initial = generate_initial_videos()
    pool = generate_video_pool(50)
    assert len(initial) == 3, "Should generate 3 initial videos"
    assert len(pool) == 50, "Should generate 50 videos"
    print(f"   ✅ Generated {len(initial)} initial videos")
    print(f"   ✅ Generated {len(pool)} video pool")
except Exception as e:
    print(f"   ❌ Video generation error: {e}")
    sys.exit(1)

# Test 3: Check environment first
print("\n3. Checking environment...")
import os
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')

# Test 4: Flask app
print("\n4. Testing Flask app...")
try:
    if not api_key or api_key == 'your_api_key_here':
        os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    from app import app
    routes = [r.rule for r in app.url_map.iter_rules() if not r.rule.startswith('/static')]
    print(f"   ✅ Flask app created with {len(routes)} routes")
    for route in routes:
        print(f"      - {route}")
except Exception as e:
    print(f"   ❌ Flask app error: {e}")
    sys.exit(1)

# Test 5: Validate API key
print("\n5. Validating API key configuration...")
if api_key and api_key != 'your_api_key_here' and api_key.startswith('sk-ant'):
    print("   ✅ ANTHROPIC_API_KEY configured correctly")
    ready = True
elif api_key == 'test-key':
    print("   ⚠️  Using test API key (app will use random recommendations)")
    ready = False
else:
    print("   ⚠️  ANTHROPIC_API_KEY not configured in .env")
    print("      App will use random recommendations as fallback")
    ready = False

print("\n" + "="*60)
if ready:
    print("✅ ALL TESTS PASSED! Ready to run the app with Claude AI.")
    print("\nStart the server with: ./start.sh")
else:
    print("⚠️  SETUP INCOMPLETE")
    print("\nTo enable Claude AI recommendations:")
    print("1. Create .env file: cp .env.example .env")
    print("2. Add your API key from: https://console.anthropic.com/")
    print("3. Run again: python test_setup.py")
    print("\nOr just run: ./start.sh (app works without API key)")

print("="*60)
