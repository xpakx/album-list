from orgparse import load
import re
import json
import argparse


def getOrgData(filename):
    note = load(filename)

    ranking = note.children[0]
    print("Getting ranking from node '{}'…".format(ranking.get_heading()))

    albumList = ranking.get_body(format="raw")

    regex = r"([0-9]+)\. (.+) [—–-] (.+) \[([0-9]+)/10\]"
    match = re.findall(regex, albumList)
    return match


def toJson(albumList, indent=None) -> str:
    keys = ["number", "artist", "title", "rating"]

    albumsNew = []
    for album in albumList:
        item = dict(zip(keys, album))
        albumsNew.append(item)

    return json.dumps(albumsNew, indent=indent)


def saveTo(data: str, filename: str):
    f = open(filename, "w")
    f.write(data)
    f.close()


def main():
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument('--out', type=str, default="output.json", help="Output file path (e.g., output.json)")
    parser.add_argument('input_file', type=str, help="Input file path (e.g., input.org)")
    args = parser.parse_args()

    albums = getOrgData(args.input_file)

    print("Albums read:      ", len(albums))
    print("Last item number: ", albums[-1][0])

    jsonAlbums = toJson(albums[:30], 4)
    saveTo(jsonAlbums, args.out)


if __name__ == "__main__":
    main()
