# Musician Raccoon 2

## Config

| Option               | Description                                                                             | Type                        | Default Value |
| -------------------- | --------------------------------------------------------------------------------------- | --------------------------- | ------------- |
| `download_path`      | Downloads folder path.                                                                  | `str`                       | `./downloads` |
| `playlists`          | List of the playlist for download.                                                      | `list[str]`                 | _not set_     |
| `cover_replacements` | The id of the song as key, with the id of the song that has the desired cover as value. | `dict[str, str]`            | _not set_     |
| `cover_art_options`  | Cover art tweaks for the song cover art.                                                | `dict[str, dict[str, str]]` | _not set_     |
