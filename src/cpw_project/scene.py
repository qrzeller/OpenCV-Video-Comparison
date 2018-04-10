import subprocess
import utils
import os


## FFMPEG
# http://www.bogotobogo.com/FFMpeg/ffmpeg_thumbnails_select_scene_iframe.php
# ffmpeg frame extractor: https://superuser.com/questions/819573/split-up-a-video-using-ffmpeg-through-scene-detection
# vsync: video sync method.
# vfr: variable frame rate.
# Debug: -v debug
# Set a threshold value between 0 and 1 for detecting a new scene.
# Increase the value to lower the number of detected scenes; sane
# values are typically between 0.3 and 0.5.
def extract_scenes(videos_path, scenes_path, ffmpeg_path):

    # Get all video file recursive
    video_files = utils.get_files_rec(videos_path)

    # Process all video
    for file in video_files:

        # Get filename and create directory to store frame about current video
        filename = utils.get_filename_we(file)
        utils.create_dir(os.path.join(scenes_path, filename))

        # Detect changing scene
        args = " -i " + file + " -vf select='gt(scene\,0.4)',showinfo -vsync vfr " + scenes_path + filename + "\\" + filename + "_f%d.png"
        path = ffmpeg_path + args
        ffmpeg_scene_detection(path)

    # Rename all scene file like => 0000x
    rename_scene_files(scenes_path)


# Given shell command, returns communication tuple of stdout and stderr
def ffmpeg_scene_detection(cmd):

    # Instantiate a startupinfo obj:
    startupinfo = subprocess.STARTUPINFO()

    # Set the use show window flag, might make conditional on being in Windows:
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # Pass as the startupinfo keyword argument:
    return subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            startupinfo=startupinfo).communicate()


def get_value(value):
    if value < 10:
        return "0000" + str(value)
    elif value < 100:
        return "000" + str(value)
    elif value < 1000:
        return "00" + str(value)
    elif value < 10000:
        return "0" + str(value)
    else:
        return str(value)


def get_new_file_name(file):
    name, ext = utils.get_file(file)
    new_file_name = name.split('_')[0] + "_f" + get_value(int(name.split("_")[1].replace("f", ""))) + ext
    return os.path.join(os.path.dirname(file), new_file_name)


def rename_scene_files(path):
    directories = [d.path for d in os.scandir(path) if d.is_dir()]
    for directory in directories:
        files = [f for f in os.scandir(directory) if f.is_file()]
        for file in files:
            os.rename(file, get_new_file_name(file.path))
