import os


YDL_DOWNLOAD_OPTS = {
    # Ignore private / deteled videos.
    "noabortonerror": True,
    # Force sanitized filenames when using it on Windows.
    "windowsfilenames": os.name == "nt",
    # Don't show output.
    "quiet": True,
    # Avoid 429.
    # "sleeprequests": 1,
    # ...
    "noplaylist": True,
    "format": "bestaudio/best",
    "outtmpl": f"./downloads/[%(channel)s] %(title)s - %(id)s.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}
