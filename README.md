# Python_Stuff
These are the python projects I did on my free time and that I often use

## [altNotifier.py](https://github.com/L-Lawliet27/Python_Stuff/blob/main/eBookPriceNotifier/altNotifier.py)
This was my second attempt at writing a script that went through a list of eBooks on Amazon and then sent an email with the ones that had a discount. I say my second because before I used gspread to go through a Google Sheet in my Drive that had each link to a specific book and visited each page with Selenium to extract the data using BeautifulSoup to fill the info in the spreadsheet as well as to compare prices.

Turns out, that wasn't a smart approach, as it went incredibly slow and was prone to crashes involving the driver as well as the smtplib library. So, I decided to start it from scratch, and instead I made a public Amazon wishlist with all these books, made a json file to store the info, and just used the driver once. Now it goes phenomenally fast and has no problem sending the email. 

Somewhat inspired by @allanburleson [Sanderson Progress Bar](https://gist.github.com/allanburleson/037bd04bdc8a208e3a61b376cb4b1884).


## [fileOrganizer.py](https://github.com/L-Lawliet27/Python_Stuff/blob/main/fileOrganizer.py)
This was a project inspired from the one made by @tuomaskivioja for his [YouTube channel](https://www.youtube.com/watch?v=NCvI-K0Gp90&list=PLuKvKzt4UKNGCCPx5ERvM0Bp6lLNtryjh&index=22&t=482s). Only, I wrote it so that it manages my folders given the path + it only creates the given folder if and only if it finds the files within the declared extensions, otherwise I would have extra folders I don't need at the moment. 


## [ytDownloader.py](https://github.com/L-Lawliet27/Python_Stuff/blob/main/ytDownloader.py)
A YouTube video and playlist downloader using the [pytube](https://pytube.io/en/latest/) library. 

I wanted the freedom of establishing a particular folder if I downloaded a single video or a playlist, so I implemented a small cli where you can specify what exactly are you downloading. So, if a playlist is downloaded, it creates a folder with its name and stores all the videos there, but if you are downloading a single video, then it's designated to the "YoutubeDownloader" folder.

Kinda wish the resolution went to 1080p[60] or at least 720p60, but that's up to those who maintain the library.

### Update [16/03/23]
I implemented the option of downloading audio from a video and from a playlist. Now, if you wonder why I utilized the [moviepy](https://pypi.org/project/moviepy/) library to do this instead of [pydub](https://pypi.org/project/pydub/) or plain-old ffmpeg, it's because I have an error downloading the latter (along with ffmpeg-python) with Homebrew as my OSX is no longer compatible with the version currently supported by Homebrew, so it's prone to have errors when downloading software using it.

So yeah, that's where I'm at. On the other side, I tried to avoid repetition as much as possible, so I combined several functions that did the same thing into one as to not clutter the code. Finally, I used [retry](https://pypi.org/project/retry/) to run my download function again up to some tries, as sometimes pytube has a bug where it cannot download/access a video, but then on the second/third try it performs normally. I don't know if it helps yet, but we'll see how it goes.


## [musicPlayer.py](https://github.com/L-Lawliet27/Python_Stuff/blob/main/musicPlayer.py)
I wanted to be able to play the downloaded audio playlist from my previous script, so I figured I'd make a general script that plays all the .mp3 files in a folder given its path, and if there are more folders there, it would check each one, save each file's absolute path, and save it on a dict to be played on a loop. 

Had to get help from ChatGPT in terms of what library to use (apparently [pygame](https://www.pygame.org/news), which I didn't expect), the correct use of the [tqdm](https://tqdm.github.io/) terminal progress bar, and some functions to further clean the title of the songs, as people on YouTube don't know s*** about naming conventions.

Oh, and to use pygame on my OSX 10.13.6, I had to download "lame" via homebrew for it to work properly.


## [Series ProgressBar](https://github.com/L-Lawliet27/Python_Stuff/tree/main/SeriesProgressBar/MainPrototype)
I wanted to create a small python app with the easiest possible GUI library I could find (I settled for [PySimpleGUI](https://www.pysimplegui.org/en/latest/)).

The main idea is that you put in the Amazon link to the eBook page for the book series you are reading or about to read, then the script takes care of loading the series into Buttons with a Bar for your progress, which increases depending on when you read an entry.

At this moment I have down the main functionality, but I still need to finish the "ReadNext" one, that tells you what to read next depending on when you purchased the next entry and when you finished the last book in the series, then compares them with the rest of the series you have and lists them in a priority list.

Lastly, this is a prototype, as I eventually plan to make it "cleaner" with a better interface, but this'll do for now.
