from pytube import Playlist, YouTube
from os import makedirs, remove
from sys import argv
from moviepy.editor import VideoFileClip

videoPath = "/Users/Andres/Movies/"
audioPath = "/Users/Andres/Music/"
defaultVideoFolder = "YouTubeDownloader"
defaultAudioFolder = "YouTubeAudioDownloader"
troublingCharacters = (":","(","[","-","—","{","/")

usage = "\nUsage: [python3] ytDownloader.py <option> <url>\n\n" + \
    "-v:  download single video\n" + \
    "-p:  download playlist\n" +\
    "-a:  download audio from video (takes a while)\n" + \
    "-m:  download audio from playlist (takes a while)\n" + \
    "-h:  this help message\n\n"


def cleanVideoTitle(videoTitle):
    title = videoTitle.replace(" ", "")
    for t in troublingCharacters:
        if t in title:
            title=title.strip().split(t)[0].rstrip()
            break
    return title
 

def getDownloadFolder(name, path):
    newDir = path+name
    makedirs(newDir, exist_ok=True)
    return newDir


def downloadPlaylist(option,url):
    playlist = Playlist(url)
    playlistTitle = playlist.title
    contentOpt=None
    if option=="-p":
        downloadFolder = getDownloadFolder(name=playlistTitle,path=videoPath)
        contentOpt="-v"
    else:
        downloadFolder = getDownloadFolder(name=playlistTitle,path=audioPath)
        #contentOpt="-a"
    
    for v in playlist.videos:
        v.title = cleanVideoTitle(v.title)
        downloadContent(option=contentOpt,url=None, video=v, folder=downloadFolder)


def downloadContent(option, url=None, video=None, folder=None):
    if url is not None:
        video = YouTube(url)
        video.title = cleanVideoTitle(video.title)
        folder = getDownloadFolder(name=defaultVideoFolder, path=videoPath) if option=="-v" \
            else getDownloadFolder(name=defaultAudioFolder, path=audioPath)
    if option=="-v":
        resolution = video.streams.get_highest_resolution()  # Only goes up to 720p
        resolution.download(folder)
    else:
        videoMP4 = video.streams.get_lowest_resolution() # As we are only interested in the audio
        pathToMP4 = videoMP4.download(folder)
        pathToMP3 = pathToMP4.replace(".mp4",".mp3")
        clip = VideoFileClip(pathToMP4) # This is because pytube downloads the audio as mp4 by defect
        clip.audio.write_audiofile(pathToMP3)
        remove(pathToMP4)



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
        option = argv[1]

        if option == "-v" or option=="-a":
            downloadContent(option, url, None, None)
        elif option =="-p" or option=="-m":
            downloadPlaylist(option, url)
        else:
            raise Exception("Invalid Option\n")
    except KeyboardInterrupt:
        print("Exited\n")
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
