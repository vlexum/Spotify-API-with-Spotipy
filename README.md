# Spotify-API-with-Spotipy
Playing with the Spotify API through the python library Spotipy 

## sync.py
Creates new playlist and populates it with all your Liked songs from Spotify.
Once it is created its will actively sync the playlist and add new liked songs.
NOT fully synchronized only looks for a change in number of songs, meaning if liking and unliking between sync intervals => incorrect behavior.
This type of problem is out of scope(for now) since I am just messing around.

#### Future
* Going forward I will add functionality for syncing with deleted songs, meaning if you unlike the song, it will be removed. 

#### Bugs
* As mentioned above, does not sync deleted songs, if you delete songs you will mess up syncing queue.
