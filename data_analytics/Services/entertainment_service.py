# services/entertainment_service.py
from .base_service import BaseService
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

class EntertainmentService(BaseService):
    def __init__(self):
        super().__init__()
        self.spotify = None

    async def initialize_spotify(self):
        if not self.spotify:
            self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                redirect_uri="http://localhost:8888/callback",
                scope="user-read-recently-played user-top-read user-library-read playlist-read-private"
            ))

    async def get_recently_played(self):
        await self.initialize_spotify()
        return self.spotify.current_user_recently_played()

    async def get_top_tracks(self):
        await self.initialize_spotify()
        return self.spotify.current_user_top_tracks()

    async def get_top_artists(self):
        await self.initialize_spotify()
        return self.spotify.current_user_top_artists()

    async def get_playlists(self):
        await self.initialize_spotify()
        return self.spotify.current_user_playlists()

    async def fetch_data(self, start_date: str, end_date: str):
        tasks = [
            self.get_recently_played(),
            self.get_top_tracks(),
            self.get_top_artists(),
            self.get_playlists()
        ]
        
        recent, top_tracks, top_artists, playlists = await asyncio.gather(*tasks)
        
        return {
            "recently_played": recent,
            "top_tracks": top_tracks,
            "top_artists": top_artists,
            "playlists": playlists
        }
