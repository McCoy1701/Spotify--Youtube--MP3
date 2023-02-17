import os
import pytube
from pyyoutube import Api
from pytube import YouTube

DESTINATION = 'youtubeDL/songs/'
ERRORS = []

def main():
    # url = 'https://www.youtube.com/playlist?list=PL6yCM6hDsiHVqIb8VSNz91Rafz16mAhji'

    # songs = videoList(url)

    # saveToFile(songs, "youtubeDL/songs.txt")

    songs = loadFromFile("youtubeDL/songs.txt")

    # print(songs)

    for i in songs:
        download(i)
        saveToFile(ERRORS, "youtubeDL/failed.txt")


def videoList(url: str):
    api = Api(api_key='AIzaSyCFpHavevxZFGkjZzZAcKsXafdvyb1n1uc')
    
    if "youtube" in url:
        playlistId = url[len("https://www.youtube.com/playlist?list="):]
    
    playlistItems = api.get_playlist_items(playlist_id=playlistId, count=None, return_json=True)

    urlList = []

    for videoId in playlistItems['items']:
        urlList.append(f"https://www.youtube.com/watch?v={videoId['contentDetails']['videoId']}")

    return urlList


def download(url: str):
    try: 
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()

        outFile = video.download(output_path=DESTINATION)
        base, ext = os.path.splitext(outFile)

        newFile = base + ".mp3"
        os.rename(outFile, newFile)
        print(yt.title)
    
    except KeyError:
        print(f"KeyError: {yt.title} {url}")
        ERRORS.append(f"KeyError: {yt.title} {url},")
    
    except pytube.exceptions.VideoPrivate:
        print(f"VideoPrivate: {yt.title} {url}")
        ERRORS.append(f"KeyError: {yt.title} {url},")
    
    except pytube.exceptions.VideoUnavailable:
        print(f"VideoUnavailable: {yt.title} {url}")
        ERRORS.append(f"VideoUnavailable: {yt.title} {url},")


def saveToFile(list, file):
    with open(file, "w") as file:
        for i in list:
            file.write(i + "\n")


def loadFromFile(fileName):
    songs = []
    with open(fileName, "r") as file:
        for i in file.readlines():
            songs.append(i.strip("\n"))
    
    return songs


if __name__=="__main__":
    main()