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
def extract_scenes(videos_path, scenes_path, ffmpeg_path, scene_threshold):

    # Create scenes path if not exists
    utils.create_dir(scenes_path)

    # Remove special char in video filename (ffmpeg => no such file or directory)
    utils.remove_special_char(videos_path)

    # Get all video file recursive
    video_files = utils.get_files_rec(videos_path)

    # Process all video
    for file in video_files:
        extract(scenes_path, ffmpeg_path, scene_threshold, file)


# Extract scene with ffmpeg
def extract(scenes_path, ffmpeg_path, scene_threshold, file):

    # Get filename and create directory to store frame about current video
    video_name = utils.get_filename_we(file)
    utils.create_dir(os.path.join(scenes_path, video_name))
    directory = os.path.join(scenes_path, video_name) + "\\"
    frame_file = os.path.join(directory, video_name + "_frame%d.png")

    # Detect changing scene
    path = ffmpeg_path + " -i " + file + " -vf select='gt(scene\," + str(scene_threshold) + ")',showinfo -vsync vfr " + frame_file
    ffmpeg_scene_detection(path)

    # Check if we have scene file extracted => otherwise extract with scene_threshold += 0.1
    if not utils.file_exists_in_directory(directory):
        scene_threshold = scene_threshold + 0.1
        extract(scenes_path, ffmpeg_path, scene_threshold, file)
    else:

        # Rename all scene file like => frame_xxxxx
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
    new_file_name = name.split('_')[0] + "_f" + get_value(int(name.split("_")[1].replace("frame", ""))) + ext
    return os.path.join(os.path.dirname(file), new_file_name)


def rename_scene_files(path):
    directories = [d.path for d in os.scandir(path) if d.is_dir()]
    for directory in directories:
        files = [f for f in os.scandir(directory) if f.is_file()]
        for file in files:
            os.rename(file, get_new_file_name(file.path))
