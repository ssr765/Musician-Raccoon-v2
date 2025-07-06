from typing import Literal, NotRequired, TypedDict


class CoverArtStyle(TypedDict):
    background: NotRequired[str]
    size: NotRequired[Literal["full", "square", "external"]]
    position: NotRequired[list[int]]


class SongConfig(TypedDict):
    cover_art_replacement: NotRequired[str]
    cover_art_style: NotRequired[CoverArtStyle]


class Config(TypedDict):
    download_path: str
    playlists: list[str]
    song_config: NotRequired[dict[str, SongConfig]]
