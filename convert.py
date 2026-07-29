import csv
import json
import re
import os

INPUT_FILE = "videos.csv"
OUTPUT_DIR = "videos"

VIDEOS_PER_FILE = 50000

os.makedirs(OUTPUT_DIR, exist_ok=True)

videos = []
file_number = 1
total = 0


def save_file(number, data):
    filename = f"{OUTPUT_DIR}/videos-{number:03d}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            separators=(",", ":")
        )

    size = os.path.getsize(filename) / 1024 / 1024

    print(
        f"{filename} | "
        f"{len(data)} videos | "
        f"{size:.2f} MB"
    )


with open(INPUT_FILE, "r", encoding="utf-8", newline="") as f:

    reader = csv.reader(f, delimiter=";")

    for row in reader:

        if len(row) < 15:
            continue

        url = row[0]
        title = row[1]
        duration_raw = row[2]
        thumbnail = row[3]
        iframe = row[4]
        tags = row[5]
        performers = row[6]
        video_id = row[7]
        category = row[8]
        quality = row[9]
        uploader = row[10]
        date = row[12]
        preview = row[13]
        views = row[14]


        duration_match = re.search(r"\d+", duration_raw)

        duration = int(duration_match.group()) if duration_match else 0


        embed_match = re.search(
            r'src="([^"]+)"',
            iframe
        )

        embed_url = (
            embed_match.group(1)
            if embed_match
            else ""
        )


        videos.append({

            "id": video_id,

            "title": title,

            "url": url,

            "embed_url": embed_url,

            "thumbnail": thumbnail,

            "preview": preview,

            "duration": duration,

            "quality": quality,

            "category": category,

            "tags": tags,

            "performers": performers,

            "uploader": uploader,

            "date": date,

            "views": views

        })


        total += 1


        if len(videos) >= VIDEOS_PER_FILE:

            save_file(
                file_number,
                videos
            )

            file_number += 1
            videos = []


if videos:
    save_file(
        file_number,
        videos
    )


print(
    f"Finished: {total} videos"
)
