import yt_dlp
import os

def download_high_quality_mp4(url, output_dir="./videos", resolution="1080"):
    """
    Download YouTube video in high quality MP4 format

    Args:
        url (str): YouTube video URL
        output_dir (str): Directory to save the video
        resolution (str): Preferred resolution (e.g., '1080', '720')
    """
    # Make sure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Configure options for high quality MP4 download
    ydl_opts = {
        # Try to get specified resolution or fallback to best available
        "format": f"bestvideo[ext=mp4][height<={resolution}]+bestaudio[ext=m4a]/best[ext=mp4][height<={resolution}]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "restrictfilenames": True,
        "noplaylist": True,
        "progress_hooks": [
            lambda d: print(
                f"Downloading: {d['status']}, " f"{d.get('_percent_str', '0%')}"
            )
        ],
        # Use high quality encoding settings
        "postprocessor_args": [
            # Video codec settings - use original if possible
            "-c:v",
            "copy",
            # Audio codec settings - ensure good quality audio
            "-c:a",
            "aac",
            "-b:a",
            "192k",
        ],
    }

    # Check available formats first
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        print(f"Video title: {info.get('title')}")
        print(f"Available qualities:")

        # Filter to show only MP4 formats
        mp4_formats = [
            f
            for f in info.get("formats", [])
            if f.get("ext") == "mp4" and f.get("height")
        ]
        mp4_formats.sort(
            key=lambda x: (x.get("height", 0), x.get("tbr", 0)), reverse=True
        )

        for f in mp4_formats[:5]:  # Show top 5 formats
            print(f"  • {f.get('height')}p (bitrate: {round(f.get('tbr', 0))}k)")

    # Download video
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\nDownload completed successfully!")
        print(f"Video saved to: {output_dir}")
    except Exception as e:
        print(f"Error downloading video: {e}")


# Example usage
if __name__ == "__main__":
    urls = ["https://www.youtube.com/watch?v=3nVFfxXpcTo&list=PLm3oDN_0_ckZeDNpjX3x8_nWqrDrfDlU7&index=1"]
    for url in urls:
        download_high_quality_mp4(url)
