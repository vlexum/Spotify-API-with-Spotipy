import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import time

# info from spotify 
# REDACTED BECAUSE THEY ARE SECRET 
client_id = "" 
client_secret = ""

# website where you can confirm key 
# does not have to be your own
redirect_uri = "http://www.vlexum.com/"

# what type of access do we need 
# more than needed 
scopes = ("user-modify-playback-state",
          "user-read-currently-playing",
          "user-read-playback-state",
          'user-library-read',
          "user-follow-modify",
          "user-follow-read",
          "user-read-recently-played",
          "user-read-playback-position",
          "user-top-read",
          "playlist-read-collaborative",
          "playlist-modify-public",
          "playlist-read-private",
          "playlist-modify-private")

# connect to API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, redirect_uri, scope = scopes))

# get user info
user = sp.me()
user_id = user["id"]

# set playlist name
playlist_name = "spotipy syncing test " + str(random.randint(10000, 90000))

# set privacy of playlist
public = True

# set if collaborative
collab = False

# must create new playlist for ease of use
new_playlist = sp.user_playlist_create(user_id, playlist_name, public, collab, "made by mr.computer")

# url of playlist to be added to
playlist_id = new_playlist["id"]

# can only get 50 songs at a time so batching necessary
batch_limit = 50

# keep track of where we are in batching process
offset = 0

# get liked playlist data of batch_limit number of songs
liked = sp.current_user_saved_tracks(batch_limit)

# find the total number of songs
total_songs = liked['total']
num_songs = total_songs

# infinite loop for syncing
sync = True
while (sync) :
    # loop while there are songs to be added
    while(num_songs > 0):
        # uses description to give update on sync process
        description = "Loading: " + str(offset) + " / " + str(total_songs) 
        sp.playlist_change_details(playlist_id, playlist_name, public, collab, description)

        # loop through song data and find uri's
        uris = list()
        for song in liked['items']:
            uris.append(song['track']['uri'])

        # add the aquired song uri's
        sp.playlist_add_items(playlist_id, uris)

        # update looping vars
        num_songs -= batch_limit
        offset = total_songs - num_songs
        liked = sp.current_user_saved_tracks(batch_limit, offset)

    # finished syncing so grab time and format
    date_dict = time.localtime()
    date_str = time.strftime("%H:%M:%S - %m/%d/%Y")

    # update description to display last synced date
    description = "Last Synced at: " + date_str
    sp.playlist_change_details(playlist_id, playlist_name, public, collab, description)\
    
    # update vars
    offset = total_songs

    # find the total number of songs
    prev_total = total_songs

    # do "nothing" while there are no new songs to be added 
    while (prev_total == total_songs):
        # set time between syncs(if wanted)
        time.sleep(300)

        # update vars
        liked = sp.current_user_saved_tracks(batch_limit, offset)
        total_songs = liked['total']

    # update num_songs since we broke out of loop and have new songs to update
    num_songs = total_songs - prev_total


