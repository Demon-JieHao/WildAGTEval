# Copyright MediaControlEnv

from .play import Play
from .pause import Pause
from .resume import Resume
from .stop import Stop
from .next import Next
from .previous import Previous
from .fast_forward import FastForward
from .rewind import Rewind
from .set_playback_speed import SetPlaybackSpeed
from .search_media import SearchMedia
from .get_media_details import GetMediaDetails
from .create_playlist import CreatePlaylist
from .add_to_playlist import AddToPlaylist
from .get_playlists import GetPlaylists
from .get_playback_status import GetPlaybackStatus
from .shuffle import Shuffle
from .search_by_artist import SearchByArtist


ALL_TOOLS = [
    Play,
    Pause,
    Resume,
    Stop,
    Next,
    Previous,
    FastForward,
    Rewind,
    SetPlaybackSpeed,
    SearchMedia,
    GetMediaDetails,
    CreatePlaylist,
    AddToPlaylist,
    GetPlaylists,
    GetPlaybackStatus,
    Shuffle,
    SearchByArtist,
]
