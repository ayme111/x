import csv
import json
import re

INPUT_FILE = "videos.csv"
OUTPUT_FILE = "videos.json"

videos = []

with open(INPUT_FILE, "r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f, delimiter=";")

    for row in reader:
        if len(row) < 15:
            continue

        url = row[0]
        title = row[1]
        duration = row[2]
        thumbnail = row[3]
        iframe = row[4]
        tags = row[5]
        performers = row[6]
        video_id = row[7]
        category = row[8]

        # Convert "614 sec" -> 614
        duration = int(re.search(r"\d+", duration).group())

        # Extract embed URL
        embed_match = re.search(r'src="([^"]+)"', iframe)
        embed_url = embed_match.group(1) if embed_match else ""

        videos.append({
            "title": title,
            "guid": video_id,
            "embed_url": embed_url,
            "thumbnail": thumbnail,
            "duration": duration,
            "categories": category,
            "tags": tags,
            "performers": performers
        })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(videos, f, indent=2, ensure_ascii=False)

print(f"Converted {len(videos)} videos to {OUTPUT_FILE}")