from sys import argv
from os import path, scandir, environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer,time
from tqdm import tqdm
import re

def cleanName(string):
    return re.sub("^[0-9]+[- ]*", "", string) if re.match("^[0-9]+[- ]*", string) else string


def loadPlaylist(folder):
    playlist = {}
    for file in scandir(folder):
        if file.is_file() and file.name.endswith(".mp3"):
            songName = cleanName(file.name)
            filePath = path.join(folder, file)
            playlist[songName.replace(".mp3","")]=filePath
        elif file.is_dir():
            subFolder = path.join(folder,file)
            playlist.update(loadPlaylist(subFolder))

    return dict(sorted(playlist.items(),key=lambda x: x[1]))


def playPlaylist(folder):
    try:
        mixer.init()
        playlist=loadPlaylist(folder)
        for songName,song in playlist.items():
            mixer.music.load(song)
            mixer.music.play()
            duration = mixer.Sound(song).get_length()
            progressBar = tqdm(range(int(duration*10)),bar_format="{l_bar}{bar}| {remaining:>5}" ,desc=songName, dynamic_ncols=True)
            for _ in progressBar:
                time.Clock().tick(10)
            mixer.music.stop()
        mixer.quit()
    except KeyboardInterrupt:
        exit()


def main():
    try:
        if len(argv) > 2:
            raise Exception(f"The usage must be: musicPlayer.py <pathToPlaylistFolder>")
        if not argv[1]:
            raise Exception("The path field cannot be empty\n")
        folder = argv[1]
        playPlaylist(folder)
    except Exception as e:
        print(f"{str(e)}\n")


if __name__ == '__main__':
    main()
  
    



