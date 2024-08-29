import json
import requests
from pathlib import Path
import time
from datetime import datetime

USER_AGENT = "AlbumList/0.1 ( github.com/xpakx/albums )"


def search_album(artist, title):
    url = "https://musicbrainz.org/ws/2/release/"
    headers = {"User-Agent": USER_AGENT}
    params = {
        "query": f'artist:"{artist}" release:"{title}"',
        "fmt": "json",
        "limit": 1
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['releases']:
            return data['releases'][0]['id']
    return None


def get_album_cover(id):
    url = f"https://coverartarchive.org/release/{id}"
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'images' in data and data['images']:
            return data['images'][0]['thumbnails']['500']
    return None


def download_image(image_url, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download image: {filename}")


def saveTo(data: str, filename: str):
    f = open(filename, "w")
    f.write(data)
    f.close()


def getCached(filename):
    cache_file = Path(filename)
    if cache_file.exists():
        with open(filename) as f:
            return json.load(f)
    return {}


def getCachedAlbum(cached, album):
    for cached_album in cached:
        if album['artist'] == cached_album['artist'] and album['title'] == cached_album['title'] and 'id' in cached_album:
            return cached_album
    return None


def checkFile(id):
    filename = f"dist/{id}.jpg"
    cover_file = Path(filename)
    return cover_file.exists()


def main():
    with open('data/albumy.json') as f:
        albums = json.load(f)
    cached = getCached('dist/albumy.json')

    for album in albums:
        artist = album['artist']
        title = album['title']

        cached_album = getCachedAlbum(cached, album)
        cached_id = cached_album['id'] if cached_album else None
        if cached_id:
            print(f"Using cached id for {artist} - {title}...")
            album['id'] = cached_id
            album['image'] = album['image'] if 'image' in album else checkFile(album['id'])
            continue

        print(f"New album: {artist} - {title}.")
        print("Fetching id...")
        album['id'] = search_album(artist, title)
        time.sleep(1)

        if int(album['number']) > 30:
            print("Position is beyond the first 30 items. Skipping cover fetching...")
            continue

        if album['id']:
            filename = f"dist/{album['id']}.jpg"
            cover_file = Path(filename)
            if not cover_file.exists():
                print("Getting album cover url...")
                cover_url = get_album_cover(album['id'])
                time.sleep(1)
                if cover_url:
                    print(f"Saving album cover in dist/{album['id']}...")
                    download_image(cover_url, filename)
                    album['image'] = True
                    time.sleep(1)
                else:
                    album['image'] = False
                    print("Cover art not found")
            else:
                album['image'] = True
                print("Cover art is already downloaded")
        else:
            album['image'] = False
            print("Album not found in MusicBrainz")

    saveTo(json.dumps(albums), "dist/albumy.json")


if __name__ == "__main__":
    main()
