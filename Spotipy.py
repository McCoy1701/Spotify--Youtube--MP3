import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


def main():
    playlists, tracks = findPlaylists('mccoy_1701')
    
    songs = findSongs(playlists, tracks, trackNumber=0)
    saveFileJson(songs, "songs.json")


def findSongs(list, tracks, trackNumber) -> list:
    uriList = findUri(list)
    
    songs = []
    offset: int = 0
    while offset < tracks[trackNumber]['total']:
        trackList = sp.playlist_tracks(uriList[trackNumber], offset=offset)
        
        for track in trackList['items']:
            songs.append(track['track']['album']['artists'][0]['name'] + ' ' + track['track']['name'])
        
        offset += 100
    
    return songs


def findPlaylists(userId: str) -> list:
    playlists = sp.user_playlists(userId)
    tracks = []
    
    for playlist in playlists['items']:
        tracks.append(playlist['tracks'])

    return playlists, tracks


def findTracks(list: list) -> list:
    uriList = findUri(list)
    trackList = sp.playlist_tracks(uriList[0], offset=0)
    return trackList


def saveFileJson(text, filename):
    with open(filename, "w", encoding="UTF-8") as file:
        for i in text:
            file.write(i + "\n")


def findUri(lists) -> list:
    uriList = []

    for list in lists['items']:
        a = list['uri']
        uriList.append(a)
    
    return uriList


if __name__ == "__main__":
    main()