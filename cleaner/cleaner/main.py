import os
import json


def main():
    with open('dist/albumy.json') as f:
        albums = json.load(f)
    ids = {album['id'] for album in albums}
    dir = 'dist/'

    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            file_id = filename[:-4]
            if file_id not in ids:
                file_path = os.path.join(dir, filename)
                print(f"Deleting {file_path}")
                os.remove(file_path)


if __name__ == "__main__":
    main()
