from orgparse import load
import re
import json


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
    albums = getOrgData('data/albumy.org')

    print("Albums read:      ", len(albums))
    print("Last item number: ", albums[-1][0])

    jsonAlbums = toJson(albums, 4)
    saveTo(jsonAlbums, 'data/albumy.json')


if __name__ == "__main__":
    main()
