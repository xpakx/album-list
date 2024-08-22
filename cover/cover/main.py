import json
import requests

USER_AGENT = "AlbumList/0.1 (github.com/xpakx/albums)"

def search_album(artist, title):
    url = "https://musicbrainz.org/ws/2/release/"
    params = {
        "query": f'artist:"{artist}" release:"{title}"',
        "fmt": "json",
        "limit": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['releases']:
            return data['releases'][0]['id']
    return None

def main():
    with open('data/albumy.json') as f:
        albums = json.load(f)
    
    for album in albums:
        artist = album['artist']
        title = album['title']
        print(f"Fetching id for {artist} - {title}...")
        album['id'] = search_album(artist, title)
        print(album['id'])

if __name__ == "__main__":
    main()
