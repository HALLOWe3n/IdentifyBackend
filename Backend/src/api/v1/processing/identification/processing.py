from Backend.src.api.root.settings import APPLE_MUSIC, SPOTIFY

from .apple_music import AppleMusicProviderSearch
from .spotify import SpotifyProviderSearch
from ...dataclasses.client import ClientResponseIdentificationModel


class Processing:
    def __init__(
        self, db, song_id: str, user_requested_provider: str, song_provider: str
    ):
        self.db = db
        self.song_id = song_id
        self.user_requested_provider = user_requested_provider
        self.song_provider = song_provider

    def __get_provider_for_start_search(self):
        providers = {
            APPLE_MUSIC: AppleMusicProviderSearch,
            SPOTIFY: SpotifyProviderSearch,
        }
        return providers.get(self.song_provider)

    def __get_all_antipodes_providers(self):
        return {APPLE_MUSIC: AppleMusicProviderSearch, SPOTIFY: SpotifyProviderSearch}

    async def identification(self):
        UserCurrentProvider = self.__get_provider_for_start_search()
        to_search_provider = UserCurrentProvider(db=self.db)
        current_song_data = await to_search_provider.search_by_id(song_id=self.song_id)
        parsed_data = to_search_provider.parsing_song_by_id(data=current_song_data)

        isrc = parsed_data["isrc"]
        all_providers = self.__get_all_antipodes_providers()

        antipodes_data_found = []

        for provider_name, ProviderClass in all_providers.items():
            if provider_name == self.song_provider:
                continue

            provider = ProviderClass(db=self.db)
            detected_data = await provider.search_by_isrc(song_isrc=isrc)
            antipodes_song_data = provider.parsing_song_by_isrc(data=detected_data)

            antipodes_data_found.append(
                {
                    "name": provider.name,
                    "data": {
                        "songID": antipodes_song_data["song_id"],
                        "isrc": antipodes_song_data["isrc"],
                        "url": antipodes_song_data["song_link"],
                        "isUserProvider": True
                        if to_search_provider.name == self.user_requested_provider
                        else False,
                    },
                }
            )

        # call Spotify api for get all track information
        spotify_song_id = None
        if isinstance(to_search_provider, SpotifyProviderSearch):
            spotify_song_id = parsed_data["song_id"]
        else:
            for antipodes in antipodes_data_found:
                if antipodes["name"] == SPOTIFY:
                    spotify_song_id = antipodes["data"]["songID"]
                    break

        info_instance = SpotifyProviderSearch(db=self.db)
        all_info_response = await info_instance.search_by_id(song_id=spotify_song_id)
        all_info = info_instance.parse_all_song_data(data=all_info_response)

        artist_id = all_info["artist_id"]
        artist_data = await info_instance.get_artist(artist_id=artist_id)
        parsed_artist = info_instance.parsing_artist(data=artist_data)

        # ..
        # Prepare Data to response
        return ClientResponseIdentificationModel(
            identification=[
                {
                    "name": to_search_provider.name,
                    "data": {
                        "songID": parsed_data["song_id"],
                        "isrc": parsed_data["isrc"],
                        "url": parsed_data["song_link"],
                        "isUserProvider": True
                        if to_search_provider.name == self.user_requested_provider
                        else False,
                    },
                },
                *antipodes_data_found,
            ],
            songInformation={
                "name": all_info["name"],
                "artists": all_info["artists"],
                "albumImage": all_info["album_image"],
                "artistImage": parsed_artist,
                "songURL": all_info["preview_song_url"],
                "musicVideoURL": "https://",
            },
        )
