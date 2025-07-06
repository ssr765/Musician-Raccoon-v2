from io import BytesIO

from PIL import Image
import eyed3
import eyed3.id3
import requests
import yaml
import yt_dlp

from config.schema import Config, SongConfig
from config.ydl_options import YDL_DOWNLOAD_OPTS
from exceptions import MusicianRaccoonError


def generate_cover(url: str, options: SongConfig | None) -> bytes:
    if options is not None and options.get("cover_art_replacement") is not None:
        replacement_id_or_url = options.get("cover_art_replacement")
        if len(replacement_id_or_url) == 11:  # type: ignore shitty linter
            with yt_dlp.YoutubeDL() as ydl:
                replacement_info = ydl.extract_info(
                    f"https://www.youtube.com/watch?v={options['cover_art_replacement']}",  # type: ignore shitty linter
                    download=False,
                )
                if replacement_info is not None:
                    url = replacement_info["thumbnail"]
        else:
            url = replacement_id_or_url  # type: ignore shitty linter

    response = requests.get(url)
    image_data = response.content

    # Miniatura
    miniatura = Image.open(BytesIO(image_data))

    background = (
        options.get("cover_art_style", {}).get("background") if options is not None else None
    )
    size = (
        options.get("cover_art_style", {}).get("size", "square")
        if options is not None
        else "square"
    )
    position = options.get("cover_art_style", {}).get("position") if options is not None else None

    # New image.
    base = Image.new(mode="RGB", size=(1280, 1280), color=background)

    # Resize and paste the image.
    if size == "square":
        miniatura = miniatura.resize((2274, 1280))
        if position is not None:
            Image.Image.paste(base, miniatura, (position[0], position[1]))
        else:
            Image.Image.paste(base, miniatura, (-497, 0))

    elif size == "full":
        Image.Image.paste(base, miniatura, (0, 280))
    elif size == "external":
        miniatura = miniatura.resize((1280, 1280))
        Image.Image.paste(base, miniatura, (0, 0))

    # Save the cover art.
    cover_data = BytesIO()
    base.save(cover_data, format="JPEG")
    return cover_data.getvalue()


def metadata_post_hook(filename: str, song: dict, options: SongConfig | None):
    cancion = eyed3.load(filename)

    if cancion is None:
        raise MusicianRaccoonError

    cover_data = generate_cover(song["thumbnail"], options)

    cancion.tag.title = song["title"]
    cancion.tag.artist = (
        ";".join(song["artists"]) if song.get("artists") is not None else song["channel"]
    )
    cancion.tag.album = song.get("album") or song["title"]
    cancion.tag.images.set(3, cover_data, "image/jpeg")  # type: ignore
    cancion.tag.save(version=eyed3.id3.ID3_V2_3)  # type: ignore


def load_config() -> Config:
    # Load config
    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file)

    return data


def main() -> None:
    # Load config
    config = load_config()
    print(config)

    songs = []

    with yt_dlp.YoutubeDL() as ydl:
        for playlist in config["playlists"]:
            playlist_data = ydl.extract_info(playlist, download=False)

            if playlist_data is None:
                continue

            songs += playlist_data["entries"]

    for song in songs:
        with yt_dlp.YoutubeDL(YDL_DOWNLOAD_OPTS) as ydl:
            options = config.get("song_config", {}).get(song["id"])
            ydl.add_post_hook(lambda filename: metadata_post_hook(filename, song, options))
            ydl.process_info(song)


if __name__ == "__main__":
    main()
