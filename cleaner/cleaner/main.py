import os
import json
import argparse

def load_ids(filename: str):
    with open(filename) as f:
        albums = json.load(f)
    return {album['id'] for album in albums}

def main():
    parser = argparse.ArgumentParser(description="Album cover cleaner")
    parser.add_argument( 'files', metavar='FILE', type=str, nargs='+', help='List of files with album data.')

    args = parser.parse_args()
    file_list = args.files
    if len(file_list) == 0:
        print("No files with album data. Aborting.")
        return

    print(file_list)
    ids = []
    for filename in file_list:
        print(f"Loading file: {filename}")
        ids.extend(load_ids(filename))

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
