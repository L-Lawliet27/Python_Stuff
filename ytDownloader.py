from pytube import Playlist, YouTube
from os import path, makedirs, rmdir
from sys import argv
from time import sleep

videoPath = "/Users/Andres/Movies/"


def getDownloadFolder(name="YouTubeDownloader"):
    newDir = path.join(videoPath, name)
    makedirs(newDir, exist_ok=True)
    return newDir


def downloadPlaylist(url):
    playlist = Playlist(url)
    playlistTitle = playlist.title
    downloadFolder = getDownloadFolder(name=playlistTitle)
    for v in playlist.videos:
        downloadVideo(url=None, video=v, folder=downloadFolder)


def downloadVideo(url=None, video=None, folder=None):
    if url is not None:
        video = YouTube(url)
        folder = getDownloadFolder()

    resolution = video.streams.get_highest_resolution()  # Only goes up to 720p
    if resolution is None:
        if url is None:
            try:
                rmdir(folder)
            except OSError:
                pass
        raise Exception("There's Not a Good Resolution\n")
    resolution.download(folder)


def main():
    try:
        if len(argv) > 3:
            raise Exception("The usage must be: downloadYT.py LINK")
        if argv[1] == "-h" or "":
            print(
                "\nUsage: [python3] ytDownloader.py <option> <url>\n\n-v: download single video\n-p: download playlist\n-h: this help message\n\n")
            exit()
        if not argv[2]:
            raise Exception("The Link Field cannot be empty\n")

        url = argv[2]

        if argv[1] == "-v":
            downloadVideo(url)
        elif argv[1] == "-p":
            downloadPlaylist(url)

    except KeyboardInterrupt:
        print("Exited\n")
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
