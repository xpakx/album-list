import json
import requests

USER_AGENT = "AlbumList/0.1 (github.com/xpakx/albums)"

def search_album(artist, title):
    url = "https://musicbrainz.org/ws/2/release/"
    headers = { "User-Agent": USER_AGENT }
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
    headers = { "User-Agent": USER_AGENT }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'images' in data and data['images']:
            return data['images'][0]['image']
    return None

def download_image(image_url, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download image: {filename}")

def main():
    with open('data/albumy.json') as f:
        albums = json.load(f)
    
    for album in albums:
        artist = album['artist']
        title = album['title']
        print(f"Fetching id for {artist} - {title}...")
        album['id'] = search_album(artist, title)

        if album['id']:
            cover_url = get_album_cover(album['id'])
            if cover_url:
                filename = f"dist/{album['id']}.jpg"
                download_image(cover_url, filename)
            else:
                print(f"Cover art not found for {artist} - {title}")
        else:
            print(f"Album not found in MusicBrainz for {artist} - {title}")

if __name__ == "__main__":
    main()
