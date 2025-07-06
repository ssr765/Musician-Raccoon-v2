from typing import TypedDict


class Config(TypedDict):
    download_path: str
    playlists: list[str]
    cover_art_options: dict[str, dict[str, str]]
