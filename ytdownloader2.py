import argparse
from pytube import YouTube
from pytube.cli import on_progress
import os
import datetime


def download_video(link, is_video, format_type, destination):
    yt = YouTube(link, on_progress_callback=on_progress)
    if is_video == "V":
        yd = yt.streams.get_highest_resolution()
    elif is_video == "M":
        yd = yt.streams.get_audio_only()

    print(f"Title: {yt.title}\nViews: {yt.views}\nLength: {yt.length // 60}:{yt.length % 60} min")
    print(f"Filesize: {yd.filesize / 1048576:.2f} MB")

    filename = f"{yt.title}.{format_type}"
    file_path = os.path.join(destination, filename)

    if os.path.exists(file_path):
        choice = input("File about to be downloaded already exists. Want to download anyway?\ny/n ")
        if choice != "y":
            exit(0)
        else:
            filename = f"{yt.title}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{format_type}"

    yd.download(destination, filename=filename)
    print("\nDownload completed!")


def main():
    default_destination = os.path.join(os.path.expanduser("~"), "Desktop", "recordings")

    parser = argparse.ArgumentParser(description="Download YouTube videos or music in mp4 or wav format")
    parser.add_argument("link", help="link to the YouTube video")
    parser.add_argument("-v", "--video", action="store_const", const="V", default="M",
                        help="download video - high quality")
    parser.add_argument("-f", "--format", default="mp4", choices=["mp4", "wav"],
                        help="choose the format of the downloaded file (mp4 or wav)")
    parser.add_argument("-d", "--destination", default=default_destination,
                        help="specify the directory where the downloaded content will be saved")
    args = parser.parse_args()

    if not os.path.exists(args.destination):
        os.makedirs(args.destination)

    download_video(args.link, args.video, args.format, args.destination)


if __name__ == '__main__':
    main()
