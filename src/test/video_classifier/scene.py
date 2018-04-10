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
def process_scene(video_files, frame_path, ffmpeg_path):

    # Process all video
    for file in video_files:

        # Get filename and create directory to store frame about current video
        filename = utils.get_filename_we(file)
        utils.create_dir(os.path.join(frame_path, filename))

        # Detect changing scene
        # TODO change frames here
        args = " -i " + file + " -vf select='gt(scene\,0.4)',showinfo -vsync vfr frames\\" + filename + "\\" + filename + "_f%d.png"
        path = ffmpeg_path + args
        ffmpeg_scene_detection(path)


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
