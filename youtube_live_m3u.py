import os
import subprocess

INPUT_FILE = "channels.txt"
OUTPUT_FILE = "YouTube_Live_Stream.m3u"

def get_live_stream_url(youtube_url):
    """Mengambil direct stream URL (.m3u8) dari link YouTube Live menggunakan yt-dlp"""
    try:
        cmd = [
            "yt-dlp",
            "--get-url",
            "--no-warnings",
            "--format", "best",
            youtube_url.strip()
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        stream_urls = result.stdout.strip().splitlines()
        return stream_urls[0] if stream_urls else None
    except subprocess.CalledProcessError:
        print(f"Gagal mengambil stream untuk: {youtube_url} (Kemungkinan sedang tidak live)")
        return None

def generate_m3u():
    if not os.path.exists(INPUT_FILE):
        print(f"File {INPUT_FILE} tidak ditemukan!")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = f.readlines()

    m3u_content = "#EXTM3U\n\n"
    success_count = 0

    for url in urls:
        url = url.strip()
        if not url or url.startswith("#"):
            continue
            
        print(f"Memeriksa: {url}")
        stream_url = get_live_stream_url(url)
        
        if stream_url:
            m3u_content += f'#EXTINF:-1 tvg-chno="{success_count + 1}" group-title="YouTube Live",YouTube Live Channel {success_count + 1}\n'
            m3u_content += f"{stream_url}\n\n"
            success_count += 1
            print(f"Berhasil menambahkan stream!")
        else:
            print(f"Stream offline atau tidak ditemukan.")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"\nSelesai! Playlist M3U disimpan di {OUTPUT_FILE} ({success_count} channel aktif).")

if __name__ == "__main__":
    generate_m3u()
