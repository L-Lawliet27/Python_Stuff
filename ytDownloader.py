from pytube import Playlist, YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from os import path, makedirs, rmdir
from sys import argv

videoPath = "/Users/Andres/Movies/"
defaultFolderName = "YouTubeDownloader"

usage = "\nUsage: [python3] ytDownloader.py <option> <url>\n\n" + \
    "-v:  download single video\n" + \
    "-p:  download playlist\n" +\
    "-h:  this help message\n\n"
 
def getDownloadFolder(name=defaultFolderName):
    newDir = path.join(videoPath, name)
    makedirs(newDir, exist_ok=True, mode=0o777)
    return newDir


def downloadPlaylist(url):
    playlist = Playlist(url)
    playlistTitle = playlist.title
    downloadFolder = getDownloadFolder(name=playlistTitle)
    for v in playlist.videos:
        downloadVideo(url=None, video=v, folder=downloadFolder)


def cleanVideoTitle(videoTitle):
    title = videoTitle.replace(" ", "")
    if ":" in title:
        title=title.replace(":", "_")
    if "(" in title:
         title=title.strip().split("(")[0].rstrip()
    if "[" in title:
        title=title.strip().split("(")[0].rstrip()
    return title


def downloadVideo(url=None, video=None, folder=None):
    if url is not None:
        video = YouTube(url)
        video.title = cleanVideoTitle(video.title)
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
            raise Exception(f"The usage must be: {usage}")
        if argv[1] == "-h" or "":
            print(usage)
            exit()
        if not argv[2]:
            raise Exception("The Link Field cannot be empty\n")

        url = argv[2]

        if argv[1] == "-v":
            downloadVideo(url)
        elif argv[1] == "-p":
            downloadPlaylist(url)
        else:
            raise Exception("Invalid Option\n")
    except KeyboardInterrupt:
        print("Exited\n")
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
