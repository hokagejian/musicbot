from os import path
import yt_dlp
from yt_dlp.utils import DownloadError

COOKIES_PATH = "BrandedXmusic.txt"  # <-- Path ke file cookies hasil ekspor browser

ytdl_opts = {
    "outtmpl": "downloads/%(id)s.%(ext)s",
    "format": "bestaudio[ext=m4a]",
    "geo_bypass": True,
    "nocheckcertificate": True,
    "cookies": COOKIES_PATH,  # <-- Tambahkan ini
}

ytdl = yt_dlp.YoutubeDL(ytdl_opts)

def download(url: str, my_hook) -> str:
    ydl_optssx = {
        "format": "bestaudio[ext=m4a]",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
        "cookies": COOKIES_PATH,  # <-- Tambahkan ini juga di sini
    }
    info = ytdl.extract_info(url, False)
    try:
        x = yt_dlp.YoutubeDL(ydl_optssx)
        x.add_progress_hook(my_hook)
        dloader = x.download([url])
    except Exception as y_e:
        print(y_e)
        return None
    else:
        dloader
    xyz = path.join("downloads", f"{info['id']}.{info['ext']}")
    return xyz
