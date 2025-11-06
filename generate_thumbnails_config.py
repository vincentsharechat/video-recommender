#!/usr/bin/env python3
"""
Script to pre-generate 1000 thumbnails and store them in thumbnails_config.json
"""

import json
from video_generator import generate_video_pool

def main():
    print("Generating 1000 thumbnails...")
    thumbnails = generate_video_pool(1000, user_history=None)

    output_file = "thumbnails_config.json"
    with open(output_file, "w") as f:
        json.dump(thumbnails, f, indent=2)

    print(f"✓ Successfully generated {len(thumbnails)} thumbnails")
    print(f"✓ Saved to {output_file}")

    # Print some statistics
    categories = {}
    for thumb in thumbnails:
        cat = thumb["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\nCategory distribution:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} ({count/len(thumbnails)*100:.1f}%)")

if __name__ == "__main__":
    main()
