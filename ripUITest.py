import os
from moviepy.editor import *
import pytube
import tkinter as tk
from tkinter import filedialog

import ctypes

# Load the user32 and kernel32 libraries
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
# Load the icon from file
icon_path = r"C:\Users\XymiA\Desktop\urlRip\sd.ico"
h_icon = user32.LoadImageW(None, icon_path, ctypes.wintypes.UINT(0x00000003), 0, 0, 0x00000010)
# Get the console window handle
hwnd = kernel32.GetConsoleWindow()

# Set the window icon
user32.SendMessageW(hwnd, 0x80, 0, h_icon)

import warnings
warnings.filterwarnings("ignore")


def download_file(url, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        local_filename = stream.download(output_path=directory)
        base, ext = os.path.splitext(local_filename)
        new_filename = base + ".mp3"
        os.rename(local_filename, new_filename)
        return new_filename
    except pytube.exceptions.PytubeError as e:
        print(f"Error downloading file: {e}")
        return None

def convert_video():
    url = url_entry.get()
    if "youtube.com" not in url and "youtu.be" not in url:
        result_label.config(text="Invalid URL, try again.")
        return
    directory = filedialog.askdirectory()
    filename = download_file(url, directory)
    if filename is None:
        result_label.config(text="Error downloading file.")
        return
    else:
        result_label.config(text=f"File {filename} downloaded successfully to {os.path.abspath(filename)}!")
    output_file = os.path.splitext(filename)[0] + ".mp3"
    try:
        try:
            video = VideoFileClip(filename, ffmpeg_params=['-hide_banner'])
        except:
            pass
        audio = video.audio
        audio.write_audiofile(output_file, '-acodec','libmp3lame')
        result_label.config(text=f"File {output_file} was converted successfully to {os.path.abspath(output_file)}!")
    except OSError as e:
        result_label.config(text=f"Error converting file: {e}")
    finally:
        if 'video' in locals():
            video.close()
        if 'audio' in locals():
            audio.close()

root = tk.Tk()
root.title("FILE RIPPER")
root.iconbitmap(r"C:\Users\XymiA\Desktop\urlRip\sd.ico")
url_label = tk.Label(root, text="Enter URL:")
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)
convert_button = tk.Button(root, text="Convert", command=convert_video)
convert_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
status_label = tk.Label(root, text="RIPS FILES FROM YOUTUBE AND CONVERTS TO MP3.")
status_label.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky="s")
result_label = tk.Label(root, text="")
result_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
root.mainloop()
