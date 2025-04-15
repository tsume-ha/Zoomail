import os
import sys
import json
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()


with open("dump.json", "r", encoding="utf-8") as f:
    data = json.load(f)

from movie.models import YoutubeURL

movie_data = [row for row in data if row["model"] == "movie.youtubeurl"]
print(f"Found {len(movie_data)} movies in dump.json")
movies = []
for row in movie_data:
    fields = row["fields"]
    movie = YoutubeURL(
        pk=row["pk"],
        title=fields["title"],
        url=fields["url"],
        textcontent=fields["textcontent"],
        held_at=datetime.date.fromisoformat(fields["held_at"]),
        created_at=datetime.datetime.fromisoformat(fields["created_at"]),
        created_by_id=fields["created_by"],
    )
    movies.append(movie)
print(f"Creating {len(movies)} movies...")
YoutubeURL.objects.bulk_create(movies)
print("Movies created.")

from photo.models import PhotoAlbum
from django.core.files.base import ContentFile

picture_data = [row for row in data if row["model"] == "pictures.album"]
print(f"Found {len(picture_data)} pictures in dump.json")
for row in picture_data:
    fields = row["fields"]
    album = PhotoAlbum(
        pk=row["pk"],
        title=fields["title"],
        url=fields["url"],
        held_at=datetime.date.fromisoformat(fields["held_at"]),
        created_at=datetime.datetime.fromisoformat(fields["created_at"]),
        created_by_id=fields["created_by"],
    )
    if fields["thumbnail"]:
        filepath = os.path.join("private_media", "old", fields["thumbnail"])
        with open(filepath, "rb") as f:
            file_content = f.read()
        content_file = ContentFile(file_content)
        album.thumbnail.save(fields["thumbnail"], content_file, save=False)
    album.save()
print("Pictures created.")
