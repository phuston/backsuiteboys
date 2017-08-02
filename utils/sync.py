import os
import re

import spotipy
import hashlib
import barcode
from barcode.writer import ImageWriter
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
username = '1225376935'

def sync():
    playlists = gen_playlist_dict()
    create_barcode_assets(playlists)

def create_barcode_assets(playlists):
    for name, tracks in playlists.iteritems():
        barcode_dir = './utils/sync-sink/{}'.format("".join([c for c in name if re.match(r'\w', c)]))
        print barcode_dir
        if not os.path.exists(barcode_dir):
            os.makedirs(barcode_dir)

        for track in tracks:
            track_filename = barcode_dir + "/" + "".join([c for c in track['name'] if re.match(r'\w', c)])
            track_barcode = barcode.get('code39', track['uri_hash'], writer=ImageWriter())
            track_barcode.save(track_filename)

def gen_playlist_dict():
    playlist_dict = {}

    playlists = sp.user_playlists(username)
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            playlist_owner = playlist['owner']['id']
            playlist_name = playlist['name']

            track_list = []

            tracks = sp.user_playlist(playlist_owner, playlist['id'])['tracks']['items']

            # Enumerate over all tra
            for item in tracks:
                track_dict = dict()
                track = item['track']
                track_dict['name'] = track['name']
                track_dict['track_artist_name'] = track['artists'][0]['name'] # TODO handle case where multiple names
                track_dict['uri'] = track['uri']
                track_dict['uri_hash'] = hashlib.md5(track['uri']).hexdigest()[:12].upper()
                track_list.append(track_dict)

            playlist_dict[playlist_name] = track_list

        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

    return playlist_dict


if __name__ == '__main__':
    sync()
